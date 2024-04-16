import os
import open3d.visualization.gui as gui

from gui.config_gui import BaseConfiguration as BaseConfigurationGUI
from gui.logger_gui import Logger

from pcd.file_io import FileIO as PCD_File_IO
from pcd.sensor_io import SensorIO as PCD_Sensor_IO
from pcd.viz import PointCloudVisualizer

from img.file_io import FileIO as IMG_File_IO
from img.sensor_io import SensorIO as IMG_Sensor_IO
from img.viz import ImageVisualizer

from calib.file_io import FileIO as CLB_File_IO
from lbl.file_io import FileIO as LBL_File_IO

import keyboard, threading, time

class LiGuard:
    def __init__(self):
        # initialize the application
        self.app = gui.Application.instance
        self.app.initialize()
        
        # initialize the configuration GUI
        self.config = BaseConfigurationGUI(self.app)
        # initialize the logger GUI
        self.logger = Logger(self.app)
        # set the callbacks for the configuration GUI
        config_call_backs = BaseConfigurationGUI.get_callbacks_dict()
        config_call_backs['apply_config'] = [self.reset, self.start]
        config_call_backs['quit_config'] = [self.quit]
        self.config.update_callbacks(config_call_backs)
        
        # initialize the data sources
        self.pcd_io = None
        self.pcd_visualizer = None
        
        self.img_io = None
        self.img_visualizer = None

        self.clb_io = None
        
        self.lbl_io = None
        
        # initialize the main lock
        self.lock = threading.Lock()
        self.is_running = False # if the app is running
        self.is_playing = False # if the frames are playing
        # initialize the data dictionary
        self.data_dict = dict()
        self.data_dict['root_path'] = os.path.abspath(os.path.curdir)
        self.data_dict['logger'] = self.logger
        self.data_dict['current_frame_index'] = 0
        self.data_dict['previous_frame_index'] = -1
        self.data_dict['maximum_frame_index'] = 0
        
        # start the application loop
        self.app.run()
        
    # handle the key events of right, left, and space keys
    def handle_key_event(self, event:keyboard.KeyboardEvent):
        if event.event_type == keyboard.KEY_DOWN:
            with self.lock:
                if event.name == 'right':
                    self.is_playing = False
                    if self.data_dict['current_frame_index'] < self.data_dict['maximum_frame_index']:
                        self.data_dict['current_frame_index'] += 1
                elif event.name == 'left':
                    self.is_playing = False
                    if self.data_dict['current_frame_index'] > 0:
                        self.data_dict['current_frame_index'] -= 1
                elif event.name == 'space':
                    self.is_playing = not self.is_playing
    
    def reset(self, cfg):
        """
        Resets the LiGuard with the given configuration.

        Parameters:
        - cfg (dict): The configuration dictionary containing the settings for LiGuard.

        Returns:
        - None
        """
        # Get the logger object from the data dictionary
        logger:Logger = self.data_dict['logger']
        # Check if the data path or logging level has changed
        need_reset = False
        need_level_change = False
        if not hasattr(self, 'last_data_path'):
            self.last_data_path = cfg['data']['path']
            need_reset = True
        if self.last_data_path != cfg['data']['path']: need_reset = True
        if not hasattr(self, 'last_logging_level'):
            self.last_logging_level = cfg['logging']['level']
            need_level_change = True
        if self.last_logging_level != cfg['logging']['level']: need_level_change = True
        if not hasattr(self, 'last_logging_path'):
            self.last_logging_path = cfg['logging']['path']
            need_reset = True
        if self.last_logging_path != cfg['logging']['path']: need_reset = True
        
        # Reset the logger if the data path or logging level has changed
        if need_reset:
            self.last_data_path = cfg['data']['path']
            self.last_logging_path = cfg['logging']['path']
            logger.reset(cfg)
        # Change the logging level if it has changed
        if need_level_change:
            self.last_logging_level = cfg['logging']['level']
            logger.change_level(cfg['logging']['level'])

        # unlock the keyboard keys right, left, and space
        keyboard.unhook_all()
        # pause at the start
        with self.lock: self.is_running = False
        # reset the frame index
        self.data_dict['previous_frame_index'] = -1
        
        # manage pcd reading
        if self.pcd_io != None: self.pcd_io.close()
        # if files are enabled
        if cfg['data']['lidar']['enabled']:
            try:
                self.pcd_io = PCD_File_IO(cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: PCD_File_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: PCD_File_IO creation failed:\n{e}', Logger.CRITICAL)
                self.pcd_io = None
        # if sensors are enabled
        elif cfg['sensors']['lidar']['enabled']:
            try:
                self.pcd_io = PCD_Sensor_IO(cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: PCD_Sensor_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: PCD_Sensor_IO creation failed:\n{e}', Logger.CRITICAL)
                self.pcd_io = None
        else: self.pcd_io = None
        # get the total number of pcd frames
        self.data_dict['total_pcd_frames'] = len(self.pcd_io) if self.pcd_io else 0
        self.logger.log(f'[main.py->LiGuard->reset]: total_pcd_frames: {self.data_dict["total_pcd_frames"]}', Logger.DEBUG)
        
        # manage pcd visualization
        if self.pcd_io and cfg['visualization']['enabled']:
            if self.pcd_visualizer != None: self.pcd_visualizer.reset(cfg)
            else:
                try:
                    self.pcd_visualizer = PointCloudVisualizer(self.app, cfg)
                    self.logger.log(f'[main.py->LiGuard->reset]: PointCloudVisualizer created', Logger.DEBUG)
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: PointCloudVisualizer creation failed:\n{e}', Logger.CRITICAL)
                    self.pcd_visualizer = None
        # manage image reading
        if self.img_io != None: self.img_io.close()
        # if files are enabled
        if cfg['data']['camera']['enabled']:
            try:
                self.img_io = IMG_File_IO(cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: IMG_File_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: IMG_File_IO creation failed:\n{e}', Logger.CRITICAL)
                self.img_io = None
        # if sensors are enabled
        elif cfg['sensors']['camera']['enabled']:
            try:
                self.img_io = IMG_Sensor_IO(cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: IMG_Sensor_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: IMG_Sensor_IO creation failed:\n{e}', Logger.CRITICAL)
                self.img_io = None
        else: self.img_io = None
        # get the total number of image frames
        self.data_dict['total_img_frames'] = len(self.img_io) if self.img_io else 0
        self.logger.log(f'[main.py->LiGuard->reset]: total_img_frames: {self.data_dict["total_img_frames"]}', Logger.DEBUG)
        
        # manage image visualization
        if self.img_io and cfg['visualization']['enabled']:
            try:
                if self.img_visualizer != None: self.img_visualizer.reset(cfg)
                else: self.img_visualizer = ImageVisualizer(self.app, cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: ImageVisualizer created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: ImageVisualizer creation failed:\n{e}', Logger.CRITICAL)
                self.img_visualizer = None

        # manage calibration reading
        if self.clb_io != None: self.clb_io.close()
        if cfg['data']['calib']['enabled']:
            try:
                self.clb_io = CLB_File_IO(cfg)
                self.logger.log(f'[main.py->LiGuard->reset]: CLB_File_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: CLB_File_IO creation failed:\n{e}', Logger.CRITICAL)
                self.clb_io = None
        else: self.clb_io = None
        # get the total number of calibration frames
        self.data_dict['total_clb_frames'] = len(self.clb_io) if self.clb_io else 0
        self.logger.log(f'[main.py->LiGuard->reset]: total_clb_frames: {self.data_dict["total_clb_frames"]}', Logger.DEBUG)
        
        # manage label reading
        if self.lbl_io != None: self.lbl_io.close()
        if cfg['data']['label']['enabled']:
            try:
                self.lbl_io = LBL_File_IO(cfg, self.clb_io.__getitem__ if self.clb_io else None)
                self.logger.log(f'[main.py->LiGuard->reset]: LBL_File_IO created', Logger.DEBUG)
            except Exception as e:
                self.logger.log(f'[main.py->LiGuard->reset]: LBL_File_IO creation failed:\n{e}', Logger.CRITICAL)
                self.lbl_io = None
        else: self.lbl_io = None
        # get the total number of label frames
        self.data_dict['total_lbl_frames'] = len(self.lbl_io) if self.lbl_io else 0
        self.logger.log(f'[main.py->LiGuard->reset]: total_lbl_frames: {self.data_dict["total_lbl_frames"]}', Logger.DEBUG)
        
        # get the maximum frame index
        self.data_dict['maximum_frame_index'] = max(self.data_dict['total_pcd_frames'], self.data_dict['total_img_frames'], self.data_dict['total_lbl_frames']) - 1
        self.logger.log(f'[main.py->LiGuard->reset]: maximum_frame_index: {self.data_dict["maximum_frame_index"]}', Logger.DEBUG)
        ##########################################
        # processes
        ##########################################
        # pre processes
        self.pre_processes = dict()
        for proc in cfg['proc']['pre']:
            if 'enabled' not in cfg['proc']['pre'][proc]: cfg['proc']['pre'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['pre'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['pre'][proc]['priority']
                    process = __import__('algo.pre', fromlist=[proc]).__dict__[proc]
                    self.pre_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: pre_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
        self.pre_processes = [self.pre_processes[priority] for priority in sorted(self.pre_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled pre_processes: {self.pre_processes}', Logger.DEBUG)
        
        # lidar processes
        self.lidar_processes = dict()
        for proc in cfg['proc']['lidar']:
            if 'enabled' not in cfg['proc']['lidar'][proc]: cfg['proc']['lidar'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['lidar'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['lidar'][proc]['priority']
                    process = __import__('algo.lidar', fromlist=[proc]).__dict__[proc]
                    self.lidar_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: lidar_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
        self.lidar_processes = [self.lidar_processes[priority] for priority in sorted(self.lidar_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled lidar_processes: {self.lidar_processes}', Logger.DEBUG)
        
        # camera processes
        self.camera_processes = dict()
        for proc in cfg['proc']['camera']:
            if 'enabled' not in cfg['proc']['camera'][proc]: cfg['proc']['camera'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['camera'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['camera'][proc]['priority']
                    process = __import__('algo.camera', fromlist=[proc]).__dict__[proc]
                    self.camera_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: camera_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
        self.camera_processes = [self.camera_processes[priority] for priority in sorted(self.camera_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled camera_processes: {self.camera_processes}', Logger.DEBUG)

        # calib processes
        self.calib_processes = dict()
        for proc in cfg['proc']['calib']:
            if 'enabled' not in cfg['proc']['calib'][proc]: cfg['proc']['calib'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['calib'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['calib'][proc]['priority']
                    process = __import__('algo.calib', fromlist=[proc]).__dict__[proc]
                    self.calib_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: calib_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
        self.calib_processes = [self.calib_processes[priority] for priority in sorted(self.calib_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled calib_processes: {self.calib_processes}', Logger.DEBUG)

        # label processes
        self.label_processes = dict()
        for proc in cfg['proc']['label']:
            if 'enabled' not in cfg['proc']['label'][proc]: cfg['proc']['label'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['label'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['label'][proc]['priority']
                    process = __import__('algo.label', fromlist=[proc]).__dict__[proc]
                    self.label_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: label_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
        self.label_processes = [self.label_processes[priority] for priority in sorted(self.label_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled label_processes: {self.label_processes}', Logger.DEBUG)
        
        # post processes
        self.post_processes = dict()
        for proc in cfg['proc']['post']:
            if 'enabled' not in cfg['proc']['post'][proc]: cfg['proc']['post'][proc]['enabled'] = 'True'
            enabled = cfg['proc']['post'][proc]['enabled']
            if enabled:
                try:
                    priority = cfg['proc']['post'][proc]['priority']
                    process = __import__('algo.post', fromlist=[proc]).__dict__[proc]
                    self.post_processes[priority] = process
                except Exception as e:
                    self.logger.log(f'[main.py->LiGuard->reset]: post_processes creation failed for {proc}:\n{e}', Logger.CRITICAL)
            
        self.post_processes = [self.post_processes[priority] for priority in sorted(self.post_processes.keys())]
        self.logger.log(f'[main.py->LiGuard->reset]: enabled post_processes: {self.post_processes}', Logger.DEBUG)
        
    def start(self, cfg):
        # start the LiGuard
        with self.lock: self.is_running = True
        
        # start key event handling
        if self.pcd_visualizer or self.img_visualizer: keyboard.hook(self.handle_key_event)
        
        # the main loop
        while True:
            # check if the app is running
            with self.lock:
                if not self.is_running: break
                # check if the frames are playing, if yes increment the frame index
                elif self.is_playing and self.data_dict['current_frame_index'] < self.data_dict['maximum_frame_index']: self.data_dict['current_frame_index'] += 1
            
            # check if the frame has changed
            frame_changed = self.data_dict['previous_frame_index'] != self.data_dict['current_frame_index']
            
            # if the frame has changed, update the data dictionary with the new frame data
            if frame_changed:
                self.data_dict['previous_frame_index'] = self.data_dict['current_frame_index']
                
                if self.pcd_io:
                    current_point_cloud_path, current_point_cloud_numpy = self.pcd_io[self.data_dict['current_frame_index']]
                    self.data_dict['current_point_cloud_path'] = current_point_cloud_path
                    self.data_dict['current_point_cloud_numpy'] = current_point_cloud_numpy
                elif 'current_point_cloud_numpy' in self.data_dict:
                    self.logger.log(f'[main.py->LiGuard->start]: current_point_cloud_numpy found in data_dict while pcd_io is None, removing ...', Logger.DEBUG)
                    self.data_dict.pop('current_point_cloud_numpy')
                
                if self.img_io:
                    current_image_path, current_image_numpy = self.img_io[self.data_dict['current_frame_index']]
                    self.data_dict['current_image_path'] = current_image_path
                    self.data_dict['current_image_numpy'] = current_image_numpy
                elif 'current_image_numpy' in self.data_dict:
                    self.logger.log(f'[main.py->LiGuard->start]: current_image_numpy found in data_dict while img_io is None, removing ...', Logger.DEBUG)
                    self.data_dict.pop('current_image_numpy')

                if self.clb_io:
                    current_calib_path, current_calib_data = self.clb_io[self.data_dict['current_frame_index']]
                    self.data_dict['current_calib_path'] = current_calib_path
                    self.data_dict['current_calib_data'] = current_calib_data
                elif 'current_calib_data' in self.data_dict:
                    self.logger.log(f'[main.py->LiGuard->start]: current_calib_data found in data_dict while clb_io is None, removing ...', Logger.DEBUG)
                    self.data_dict.pop('current_calib_data')
                
                if self.lbl_io:
                    current_label_path, current_label_list = self.lbl_io[self.data_dict['current_frame_index']]
                    self.data_dict['current_label_path'] = current_label_path
                    self.data_dict['current_label_list'] = current_label_list
                elif 'current_label_list' in self.data_dict:
                    self.logger.log(f'[main.py->LiGuard->start]: current_label_list found in data_dict while lbl_io is None, removing ...', Logger.DEBUG)
                    self.data_dict.pop('current_label_list')

                # if non of the data sources are available, exit the app in 5 seconds
                if not any([self.pcd_io, self.img_io, self.clb_io, self.lbl_io]):
                    self.logger.log(f'[main.py->LiGuard->start]: no data source is available, exiting in 5 seconds...', Logger.CRITICAL)
                    time.sleep(5)
                    break

                # apply the processes
                for proc in self.pre_processes:
                    try: proc(self.data_dict, cfg)
                    except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: pre_processes failed for {proc}:\n{e}', Logger.ERROR)
            
                if self.pcd_io:
                    for proc in self.lidar_processes:
                        try: proc(self.data_dict, cfg)
                        except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: lidar_processes failed for {proc}:\n{e}', Logger.ERROR)
                if self.img_io:
                    for proc in self.camera_processes:
                        try: proc(self.data_dict, cfg)
                        except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: camera_processes failed for {proc}:\n{e}', Logger.ERROR)
                if self.clb_io:
                    for proc in self.calib_processes:
                        try: proc(self.data_dict, cfg)
                        except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: calib_processes failed for {proc}:\n{e}', Logger.ERROR)
                if self.lbl_io:
                    for proc in self.label_processes:
                        try: proc(self.data_dict, cfg)
                        except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: label_processes failed for {proc}:\n{e}', Logger.ERROR)
                
                for proc in self.post_processes:
                    try: proc(self.data_dict, cfg)
                    except Exception as e: self.logger.log(f'[main.py->LiGuard->start]: post_processes failed for {proc}:\n{e}', Logger.ERROR)

                # update the visualizers
                if self.pcd_io:
                    if cfg['visualization']['enabled']: self.pcd_visualizer.update(self.data_dict)
                    self.pcd_visualizer.redraw()
                if self.img_io:
                    if cfg['visualization']['enabled']: self.img_visualizer.update(self.data_dict)
                    self.img_visualizer.redraw()

                if cfg['visualization']['enabled'] == False:
                    self.logger.log(f'[main.py->LiGuard->start]: Processed frame {self.data_dict["current_frame_index"]}', Logger.INFO)
                    
            else:
                # if the frame has not changed, redraw the visualizers only no processing is required
                if self.pcd_io: self.pcd_visualizer.redraw()
                if self.img_io: self.img_visualizer.redraw()
            
            # sleep for a while
            time.sleep(cfg['threads']['vis_sleep'])
            
    def quit(self, cfg):
        # stop the app
        with self.lock: self.is_running = False
        # unhook the keyboard keys
        keyboard.unhook_all()
        
        # close the data sources
        if self.pcd_io: self.pcd_io.close()
        if self.img_io: self.img_io.close()
        if self.lbl_io: self.lbl_io.close()
        
        # close the visualizers
        if self.pcd_visualizer: self.pcd_visualizer.quit()
        if self.img_visualizer: self.img_visualizer.quit()
        
        # close app
        self.app.quit()
        self.logger('LiGuard exited safely.', Logger.INFO)
        
def main():
    LiGuard()

main()