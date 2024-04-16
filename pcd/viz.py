import open3d as o3d
import numpy as np

from pcd.utils import create_pcd

from gui.logger_gui import Logger

import open3d as o3d
import numpy as np

class PointCloudVisualizer:
    """
    Class for visualizing point clouds and bounding boxes using Open3D.
    """

    def __init__(self, app, cfg: dict):
        """
        Initializes the PointCloudVisualizer.

        Args:
            app: The application object.
            cfg: A dictionary containing configuration parameters.
        """
        self.app = app
        # create visualizer
        self.viz = o3d.visualization.Visualizer()
        self.viz.create_window("PointCloud Feed", width=1000, height=1080, left=480, top=30)
        # init
        self.reset(cfg, True)
        
    def reset(self, cfg, reset_bounding_box=False):
        """
        Resets the visualizer.

        Args:
            cfg: A dictionary containing configuration parameters.
            reset_bounding_box: Whether to reset the bounding box or not.
        """
        self.cfg = cfg
        # clear geometries
        self.geometries = dict()
        self.viz.clear_geometries()
        # set render options
        render_options = self.viz.get_render_option()
        render_options.point_size = cfg['visualization']['lidar']['point_size']
        render_options.background_color = cfg['visualization']['lidar']['space_color']
        # add default geometries
        self.__add_default_geometries__(reset_bounding_box)
        
    def __add_default_geometries__(self, reset_bounding_box):
        """
        Adds default geometries to the visualizer.

        Args:
            reset_bounding_box: Whether to reset the bounding box or not.
        """
        # add coordinate frame
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame()
        self.__add_geometry__('coordinate_frame', coordinate_frame, reset_bounding_box)

        # add default range bound
        default_bound = o3d.geometry.AxisAlignedBoundingBox([-50, -50, -5], [+50, +50, +5])
        default_bound.color = self.cfg['visualization']['lidar']['bound_color']
        self.__add_geometry__('bound', default_bound, reset_bounding_box)

        # if crop enabled, remove default bound and add bound according to crop params
        if self.cfg['proc']['lidar']['crop']['enabled']:
            crop_bound = o3d.geometry.AxisAlignedBoundingBox(self.cfg['proc']['lidar']['crop']['min_xyz'], self.cfg['proc']['lidar']['crop']['max_xyz'])
            crop_bound.color = self.cfg['visualization']['lidar']['bound_color']
            self.__add_geometry__('bound', crop_bound, reset_bounding_box)
        else:
            self.viz.remove_geometry(default_bound, False)
        
        # global point cloud
        self.point_cloud = create_pcd(np.zeros((1000, 4)))
        self.__add_geometry__('point_cloud', self.point_cloud, reset_bounding_box)
        
        # bboxes
        self.bboxes = []
        
    def __add_geometry__(self, name, geometry, reset_bounding_box):
        """
        Adds a geometry to the visualizer.

        Args:
            name: The name of the geometry.
            geometry: The geometry object.
            reset_bounding_box: Whether to reset the bounding box or not.
        """
        if name in self.geometries:
            self.viz.remove_geometry(self.geometries[name], reset_bounding_box=False)
        else:
            self.geometries[name] = geometry
        self.viz.add_geometry(geometry, reset_bounding_box=reset_bounding_box)
        
    def __update_geometry__(self, name, geometry):
        """
        Updates a geometry in the visualizer.

        Args:
            name: The name of the geometry.
            geometry: The updated geometry object.

        Returns:
            bool: True if the geometry was updated successfully, False otherwise.
        """
        if name in self.geometries:
            self.viz.update_geometry(geometry)
            return True
        return False
        
    def update(self, data_dict):
        """
        Updates the visualizer with new data.

        Args:
            data_dict: A dictionary containing the data to be visualized.
        """
        if 'logger' in data_dict: logger:Logger = data_dict['logger']
        else: print('[CRITICAL ERROR]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return
        if "current_point_cloud_numpy" not in data_dict:
            logger.log(f'[pcd->viz.py->PointCloudVisualizer->update]: current_point_cloud_numpy not found in data_dict', Logger.DEBUG)
            return
        self.point_cloud.points = o3d.utility.Vector3dVector(data_dict['current_point_cloud_numpy'][:, 0:3])
        if 'current_point_cloud_point_colors' in data_dict:
            self.point_cloud.colors = o3d.utility.Vector3dVector(data_dict['current_point_cloud_point_colors'][:, 0:3])
        else:
            self.point_cloud.paint_uniform_color([1,1,1])
        self.__update_geometry__('point_cloud', self.point_cloud)
        
        self.__clear_bboxes__()
        if "current_label_list" not in data_dict:
            return
        for lbl in data_dict['current_label_list']:
            self.__add_bbox__(lbl)
            self.__add_cluster__(lbl)

    def __add_bbox__(self, label_dict: dict):
        """
        Adds a bounding box to the visualizer.

        Args:
            label_dict: A dictionary containing the label information.
        """
        if 'lidar_bbox' not in label_dict:
            return
        # bbox params
        lidar_bbox_dict = label_dict['lidar_bbox']
        lidar_xyz_center = lidar_bbox_dict['lidar_xyz_center']
        lidar_xyz_extent = lidar_bbox_dict['lidar_xyz_extent']
        lidar_xyz_euler_angles = lidar_bbox_dict['lidar_xyz_euler_angles']
        if lidar_bbox_dict['predicted']:
            color = lidar_bbox_dict['rgb_bbox_color']
        else:
            color = lidar_bbox_dict['rgb_bbox_color'] * 0.5 # darken the color for ground truth

        # calculating bbox
        rotation_matrix = o3d.geometry.OrientedBoundingBox.get_rotation_matrix_from_xyz(lidar_xyz_euler_angles)
        lidar_xyz_bbox = o3d.geometry.OrientedBoundingBox(lidar_xyz_center, rotation_matrix, lidar_xyz_extent)
        lidar_xyz_bbox.color = color
        
        self.bboxes.append(lidar_xyz_bbox)
        self.__add_geometry__(f'bbox_{str(len(self.bboxes)+1).zfill(4)}', lidar_xyz_bbox, False)
        
    def __clear_bboxes__(self):
        """
        Clears all the bounding boxes from the visualizer.
        """
        for bbox in self.bboxes:
            self.viz.remove_geometry(bbox, False)
        self.bboxes.clear()

    def __add_cluster__(self, label_dict: dict):
        """
        Adds a cluster to the visualizer.

        Args:
            label_dict: A dictionary containing the label information.
        """
        if 'lidar_cluster' not in label_dict:
            return
        # cluster params
        lidar_cluster_dict = label_dict['lidar_cluster']
        point_indices = lidar_cluster_dict['point_indices']
        colors = np.asarray(self.point_cloud.colors)
        if colors.shape[0] != point_indices.shape[0]:
            colors = np.zeros_like(self.point_cloud.points)
        colors[point_indices] = np.random.rand(3) # ToDO: use consistent color if tracking is enabled
        self.point_cloud.colors = o3d.utility.Vector3dVector(colors)
        
    def redraw(self):
        """
        Redraws the visualizer.
        """
        self.viz.poll_events()
        self.viz.update_renderer()
        
    def quit(self):
        """
        Quits the visualizer.
        """
        self.viz.destroy_window()