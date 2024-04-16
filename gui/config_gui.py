import open3d.visualization.gui as gui

import os
import time
import yaml
import ast

class BaseConfiguration:
    def get_callbacks_dict():
        """
        Returns a dictionary containing callback functions for different actions.

        Returns:
            dict: A dictionary with keys representing different actions and values as empty lists.
        """
        return {
            'new_config': [],       # List to store callback functions for 'new_config' action
            'open_config': [],      # List to store callback functions for 'open_config' action
            'save_config': [],      # List to store callback functions for 'save_config' action
            'save_as_config': [],   # List to store callback functions for 'save_as_config' action
            'apply_config': [],     # List to store callback functions for 'apply_config' action
            'quit_config': []       # List to store callback functions for 'quit_config' action
        }
    def get_callbacks_dict():
        return {'new_config': [],
                'open_config': [],
                'save_config': [],
                'save_as_config': [],
                'apply_config': [],
                'quit_config': []}
        
    def __init__(self, app: gui.Application, callbacks = get_callbacks_dict()):
        """
        Initializes the ConfigGUI class.

        Parameters:
        - app (gui.Application): The application object.
        - callbacks (dict): A dictionary of callbacks.

        Returns:
        - None
        """
        self.app = app
        
        self.mwin = app.create_window("Configuration", 480, 1080, x=0, y=30)
        self.em = self.mwin.theme.font_size
        self.callbacks = callbacks
        self.mwin.set_on_close(self.__quit_config__)
        
        self.__init__layout__()
        
    def __init__layout__(self):
        # base container
        self.base_container = gui.ScrollableVert(self.em * 0.2, gui.Margins(self.em * 0.4, self.em * 0.4, self.em * 0.4, self.em * 0.4))
        
        # file_io controls
        # -- define text edit
        self.config_file_path_textedit =  gui.TextEdit()
        self.config_file_path_textedit.text_value = "None"
        self.config_file_path_textedit.enabled = False
        #   add to file_io container
        self.base_container.add_child(self.config_file_path_textedit)
        # buttons for new, open, save, save as, and apply
        # -- define buttons
        button_container = gui.Horiz(self.em * 0.2)
        self.new_config_button = gui.Button("New")
        self.open_config_button = gui.Button("Open")
        self.save_config_button = gui.Button("Save")
        self.save_as_config_button = gui.Button("Save As")
        self.apply_config_button = gui.Button("Apply")
        # -- set callbacks
        self.new_config_button.set_on_clicked(self.__new_config__)
        self.open_config_button.set_on_clicked(self.__open_config__)
        self.save_config_button.set_on_clicked(self.__save_config__)
        self.save_as_config_button.set_on_clicked(self.__save_as_config__)
        self.apply_config_button.set_on_clicked(self.__apply_config__)
        # -- add to button container
        button_container.add_stretch()
        button_container.add_child(self.new_config_button)
        button_container.add_child(self.open_config_button)
        button_container.add_child(self.save_config_button)
        button_container.add_child(self.save_as_config_button)
        button_container.add_child(self.apply_config_button)
        # add to base container
        self.base_container.add_child(button_container)
        
        # all the generated configuration gui will be set here
        self.generated_config = gui.WidgetProxy()
        self.generated_config_gui_dict = dict()
        # add to base container
        self.base_container.add_child(self.generated_config)
        
        # add to main window
        self.mwin.add_child(self.base_container)
        
    def update_callbacks(self, callbacks):
        """
        Update the callbacks for the GUI.

        Parameters:
        callbacks (dict): A dictionary containing the callbacks for the GUI.

        Returns:
        None
        """
        self.callbacks = callbacks
        
    def load_config(self, cfg_path):
        """
        Load a configuration file.

        Args:
            cfg_path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration as a dictionary.
        """
        with open(cfg_path) as f:
            cfg = yaml.safe_load(f)
        return cfg
    
    def save_config(self, cfg, cfg_path):
        """
        Save the configuration to a YAML file.

        Args:
            cfg (dict): The configuration dictionary to be saved.
            cfg_path (str): The path to the YAML file.

        Returns:
            None
        """
        with open(cfg_path, 'w') as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
            
    def __update_config_gui_from_cfg__(self, item, container, parent_keys=[], margin=0.2):
        G = self.generated_config_gui_dict
        if type(item) == dict:
            for key in item.keys():
                label_text = key
                if type(item[key]) == dict:
                    collapsable_container = gui.CollapsableVert(label_text, self.em * 0.2, gui.Margins(self.em * margin, self.em * 0.2, self.em * 0.2, self.em * 0.2))
                    self.__update_config_gui_from_cfg__(item[key], collapsable_container, parent_keys + [key], margin + 0.2)
                    container.add_child(collapsable_container)
                elif type(item[key]) in [str, int, float]:
                    sub_container = gui.Horiz()
                    sub_container.add_child(gui.Label(label_text + ":"))
                    global_key = ".".join(parent_keys + [key])
                    G[global_key] = {'view': gui.TextEdit(), 'type': type(item[key])}
                    G[global_key]['view'].text_value = str(item[key])
                    sub_container.add_child(G[global_key]['view'])
                    container.add_child(sub_container)
                elif type(item[key]) == list:
                    sub_container = gui.Horiz()
                    sub_container.add_child(gui.Label(label_text + ":"))
                    global_key = ".".join(parent_keys + [key])
                    G[global_key] = {'view': gui.TextEdit(), 'type': type(item[key][0])}
                    G[global_key]['view'].text_value = str(item[key])
                    sub_container.add_child(G[global_key]['view'])
                    container.add_child(sub_container)
                elif type(item[key]) == bool:
                    sub_container = gui.Horiz()
                    sub_container.add_child(gui.Label(label_text + ":"))
                    global_key = ".".join(parent_keys + [key])
                    G[global_key] = {'view': gui.Checkbox(key), 'type': type(item[key])}
                    G[global_key]['view'].checked = item[key]
                    sub_container.add_child(G[global_key]['view'])
                    container.add_child(sub_container)
                else:
                    raise Exception("Unsupported type: {}".format(type(item[key])))
                
    def __update_cfg_from_gui__(self, item, parent_keys=[]):
        G = self.generated_config_gui_dict
        # Check if the item is a dictionary
        if type(item) == dict:
            # Iterate over all keys in the dictionary
            for key in item.keys():
                # Create a global key by joining the parent keys and the current key
                global_key = ".".join(parent_keys + [key])
                # If the value of the current key is a dictionary, recursively call the function
                if type(item[key]) == dict:
                    self.__update_cfg_from_gui__(item[key], parent_keys + [key])
                # If the value of the current key is a string, integer or float
                elif type(item[key]) in [str, int, float]:
                    # Update the value of the key in the item dictionary with the value from the GUI
                    item[key] = G[global_key]['type'](G[global_key]['view'].text_value)
                # If the value of the current key is a list
                elif type(item[key]) == list:
                    # Parse the list from the string value in the GUI
                    item[key] = ast.literal_eval(G[global_key]['view'].text_value)
                    # Convert each item in the list to the appropriate type
                    item[key] = [G[global_key]['type'](i) for i in item[key]]    
                # If the value of the current key is a boolean
                elif type(item[key]) == bool:
                    # Update the value of the key in the item dictionary with the checked state from the GUI
                    item[key] = G[global_key]['type'](G[global_key]['view'].checked)
                # If the value of the current key is of an unsupported type
                else:
                    # Raise an exception
                    raise Exception("Unsupported type: {}".format(type(item[key])))
                
    def __show_issue_dialog__(self):
        # create a dialog
        dialog = gui.Dialog("Configuration GUI")
        horiz = gui.Horiz(0, gui.Margins(self.em * 0.6, self.em * 0.6, self.em * 0.6, self.em * 0.4))
        horiz.add_child(gui.Label(self.issue_text))
        dialog.add_child(horiz)
        # show the dialog
        self.mwin.show_dialog(dialog)
        
    def __close_issue_dialog__(self):
        self.mwin.close_dialog()
        
    def __new_config__(self):
        # Load the default configuration
        self.cfg = self.load_config(os.path.join('configs', 'config_template.yml'))
        self.config_file_path_textedit.text_value = os.path.join('configs', time.strftime("%Y%m%d-%H%M%S") + ".yml")
        cfg_gui = gui.Vert(self.em * 0.2, gui.Margins(self.em * 0.2, self.em * 0.2, self.em * 0.2, self.em * 0.2))
        # Generate the configuration GUI from the configuration dictionary
        self.__update_config_gui_from_cfg__(self.cfg, cfg_gui, ['cfg'])
        self.generated_config.set_widget(cfg_gui)
        
        for callback in self.callbacks['new_config']: callback(self.cfg)
            
    def __open_config__(self):
        # Define the function to load the configuration file and close the dialog
        def load_cfg_and_close_dialog(cfg_path):
            self.config_file_path_textedit.text_value = cfg_path
            self.mwin.close_dialog()
            
            self.cfg = self.load_config(cfg_path)
            cfg_gui = gui.Vert(self.em * 0.2, gui.Margins(self.em * 0.2, self.em * 0.2, self.em * 0.2, self.em * 0.2))
            self.__update_config_gui_from_cfg__(self.cfg, cfg_gui, ['cfg'])
            self.generated_config.set_widget(cfg_gui)

        # Open the configuration file
        read_config_file_dialog = gui.FileDialog(gui.FileDialog.OPEN, "Load Configuration", self.mwin.theme)
        read_config_file_dialog.add_filter(".yml", "LiGuard Configuration (.yml)")
        read_config_file_dialog.set_on_cancel(lambda: self.mwin.close_dialog())
        read_config_file_dialog.set_on_done(lambda path: load_cfg_and_close_dialog(path))
        self.mwin.show_dialog(read_config_file_dialog)
        
        for callback in self.callbacks['open_config']: callback(self.cfg)
    
    def __save_config__(self):
        try:
            # Update the configuration from the GUI
            self.__update_cfg_from_gui__(self.cfg, ['cfg'])
            self.save_config(self.cfg, self.config_file_path_textedit.text_value)
        except:
            # If an exception occurs, set the issue text and show the issue dialog
            self.issue_text = "Failed to save configuration file."
            self.__show_issue_dialog__()
            time.sleep(self.cfg['threads']['vis_sleep'])
            self.__close_issue_dialog__()
        # Call the callback functions for the 'save_config' action
        for callback in self.callbacks['save_config']: callback(self.cfg)
            
    def __save_as_config__(self):
        def save_cfg_and_close_dialog(cfg, cfg_path):
            self.config_file_path_textedit.text_value = cfg_path
            self.__update_cfg_from_gui__(self.cfg, ['cfg'])
            self.save_config(cfg, cfg_path)
            self.mwin.close_dialog()
            
        if hasattr(self, 'cfg'):
            # Save the configuration to the specified path
            save_as_config_file_dialog = gui.FileDialog(gui.FileDialog.SAVE, "Save Configuration", self.mwin.theme)
            save_as_config_file_dialog.add_filter(".yml", "LiGuard Configuration (.yml)")
            save_as_config_file_dialog.set_on_cancel(lambda: self.mwin.close_dialog())
            save_as_config_file_dialog.set_on_done(lambda path: save_cfg_and_close_dialog(self.cfg, path))
            self.mwin.show_dialog(save_as_config_file_dialog)
        
        # Call the callback functions for the 'save_as_config' action
        for callback in self.callbacks['save_as_config']: callback(self.cfg)
            
    def __apply_config__(self):
        self.__update_cfg_from_gui__(self.cfg, ['cfg'])
        # Call the callback functions for the 'apply_config' action
        for callback in self.callbacks['apply_config']: callback(self.cfg)
        
    def __quit_config__(self):
        print("Quitting...")
        # Call the callback functions for the 'quit_config' action
        for callback in self.callbacks['quit_config']: callback(self.cfg)
        return True