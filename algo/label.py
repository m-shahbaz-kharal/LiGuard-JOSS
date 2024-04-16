# contains the algorithms that are used to manipulate both the read and predicted labels

import numpy as np
import open3d as o3d

from gui.logger_gui import Logger
from typing import Dict, List
import numpy as np

def remove_out_of_bound_labels(data_dict: Dict[str, any], cfg_dict: Dict[str, any]):
    """
    Remove labels that are out of the specified bounding box.

    Args:
        data_dict (Dict[str, any]): A dictionary containing data and logger.
        cfg_dict (Dict[str, any]): A dictionary containing configuration parameters.

    Returns:
        None
    """
    # Get logger object from data_dict
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->label.py->remove_out_of_bound_labels]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return

    # Check if required data is present in data_dict
    if "current_label_list" not in data_dict:
        logger.log('[algo->label.py->remove_out_of_bound_labels]: current_label_list not found in data_dict', Logger.ERROR)
        return
    
    # Get label list and bounding box limits
    lbl_list = data_dict['current_label_list']
    min_xyz = cfg_dict['proc']['lidar']['crop']['min_xyz']
    max_xyz = cfg_dict['proc']['lidar']['crop']['max_xyz']
    output = []

    for lbl_dict in lbl_list:
        if 'lidar_bbox' not in lbl_dict: continue
        bbox_center = lbl_dict['lidar_bbox']['lidar_xyz_center']
        # Check if the bounding box center is within the specified limits
        x_condition = np.logical_and(min_xyz[0] <= bbox_center[0], bbox_center[0] <= max_xyz[0])
        y_condition = np.logical_and(min_xyz[1] <= bbox_center[1], bbox_center[1] <= max_xyz[1])
        z_condition = np.logical_and(min_xyz[2] <= bbox_center[2], bbox_center[2] <= max_xyz[2])
        # If the bounding box center is within the limits, add the label to the output list
        if x_condition and y_condition and z_condition:
            output.append(lbl_dict)
        
    # Update the label list in data_dict
    data_dict['current_label_list'] = output

