import open3d.visualization.gui as gui

import os
import time
import yaml

class Logger:
    # Logging levels
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
    # Logging level strings and colors
    __level_string__ = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    __level_color__ = [gui.Color(255,255,255,255), gui.Color(0,255,0,255), gui.Color(255,255,0,255), gui.Color(255,0,0,255), gui.Color(255,0,255,255)]
    
    def __init__(self, app: gui.Application = None):
            """
            Initializes the LoggerGUI object.

            Args:
                app (gui.Application): The GUI application object.

            Returns:
                None
            """
            self.app = app

            if self.app:
                # Default log file path
                self.mwin = app.create_window("Log", 440, 1080, x=1480, y=30)
                self.em = self.mwin.theme.font_size

                self.mwin.set_on_close(lambda: False)

                self.__init__layout__()
                self.mwin.post_redraw()
        
    def reset(self, cfg: dict):
        """
        Resets the logger configuration based on the provided dictionary.

        Args:
            cfg (dict): The dictionary containing the logger configuration.

        Returns:
            None
        """
        level = cfg['logging']['level']
        path = cfg['logging']['path']
        
        if not os.path.exists(path):
            if '.txt' in path: os.makedirs(os.path.dirname(path), exist_ok=True)
            else: os.makedirs(path, exist_ok=True)
        
        if os.path.isdir(path): self.log_file_path = os.path.join(path, time.strftime("log_%Y%m%d-%H%M%S") + ".txt")
        else: self.log_file_path = path

        if level < Logger.DEBUG or level > Logger.CRITICAL:
            level = Logger.DEBUG
            self.log(f'[gui->logger_gui.py->Logger]: Invalid logging level. Setting to default level: {Logger.__level_string__[level]}', Logger.INFO)
        self.level = level

        self.log('\n\nConfiguartion:\n\n' + yaml.dump(cfg) + '\n\nLog:\n\n', Logger.DEBUG)
        self.__clear_log__()

    def change_level(self, level:int):
            """
            Change the logging level of the logger.

            Args:
                level (int): The new logging level.

            Returns:
                None
            """
            self.level = level
            self.log(f'[gui->logger_gui.py->Logger]: Logging level changed to {Logger.__level_string__[level]}', Logger.WARNING)

    def log(self, message:str, level:int):
        """
        Logs a message with the specified level.

        Args:
            message (str): The message to be logged.
            level (int): The level of the log message.

        Returns:
            None
        """

        # Write to log file
        txt = f'{time.strftime("%Y-%m-%d %H:%M:%S")} [{Logger.__level_string__[level]}] {message}\n'
        with open(self.log_file_path, 'a') as log_file: log_file.write(txt)
        
        if level < self.level: return

        if hasattr(self, 'mwin') == False:
            print(txt)
            return
        
        
        # update log container if level is greater than or equal to the current level
        horiz = gui.Horiz(self.em * 0.2, gui.Margins(self.em * 0.2, self.em * 0.2, self.em * 0.2, self.em * 0.2))
        icon_str = gui.Label(Logger.__level_string__[level])
        icon_str.text_color = Logger.__level_color__[level]
        msg_str = gui.Label(message)
        horiz.add_child(icon_str)
        horiz.add_child(msg_str)
        self.log_container.add_child(horiz)
        # request redraw
        self.mwin.set_needs_layout()
        self.mwin.post_redraw()
        
    def __init__layout__(self):
        # Create the layout for the logger window
        self.base_container = gui.Vert(self.em * 0.2, gui.Margins(self.em * 0.4, self.em * 0.4, self.em * 0.4, self.em * 0.4))
        self.log_container = gui.WidgetProxy()
        
        # Create a scrollable container for the log messages
        scroll_vert = gui.ScrollableVert(self.em * 0.2, gui.Margins(self.em * 0.2, self.em * 0.2, self.em * 0.2, self.em * 0.2))
        self.log_container.set_widget(scroll_vert)
        self.button_container = gui.Horiz(self.em * 0.2, gui.Margins(self.em * 0.4, self.em * 0.4, self.em * 0.4, self.em * 0.4))
        
        # Create a clear button
        clear_button = gui.Button("Clear")
        clear_button.set_on_clicked(self.__clear_log__)
        self.button_container.add_child(clear_button)
        self.button_container.add_stretch()

        # Add the containers to the base container
        self.base_container.add_child(self.button_container)
        self.base_container.add_child(self.log_container)
        
        # Add the base container to the main window
        self.mwin.add_child(self.base_container)
        
    def __clear_log__(self):
        if hasattr(self, 'mwin') == False: return
        # Clear the log messages by recreeating the log container
        scroll_vert = gui.ScrollableVert(self.em * 0.2, gui.Margins(self.em * 0.2, self.em * 0.2, self.em * 0.2, self.em * 0.2))
        self.log_container.set_widget(scroll_vert)

    def __quit__(self):
        self.mwin.close()
