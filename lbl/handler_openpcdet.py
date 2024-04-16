import os
import numpy as np

colors = {'Green': [0, 1, 0]}
label_file_extension = '.txt'

import os
import numpy as np

def Handler(label_path: str, calib_data: dict):
    """
    Process the label file and convert it into a list of dictionaries representing the labels.

    Args:
        label_path (str): The path to the label file.
        calib_data (dict): Calibration data.

    Returns:
        list: A list of dictionaries representing the labels.
    """
    output = []
    
    # Check if the label file exists
    if os.path.exists(label_path) == False:
        return output
    
    # Read the label file
    with open(label_path, 'r') as f:
        lbls = f.readlines()
    
    for line in lbls:
        parts = line.strip().split(' ')
        xyz_dxdydz_rz = np.array([float(i) for i in parts[0:7]], dtype=np.float32)
        obj_class = parts[7]
        
        # Create a dictionary to store the label information
        label = dict()
        label['x'] = xyz_dxdydz_rz[0]
        label['y'] = xyz_dxdydz_rz[1]
        label['z'] = xyz_dxdydz_rz[2]
        label['dx'] = xyz_dxdydz_rz[3]
        label['dy'] = xyz_dxdydz_rz[4]
        label['dz'] = xyz_dxdydz_rz[5]
        label['heading_angle'] = xyz_dxdydz_rz[6]
        label['category_name'] = obj_class
        
        lidar_xyz_center = xyz_dxdydz_rz[0:3]
        lidar_xyz_extent = xyz_dxdydz_rz[3:6]
        lidar_xyz_euler_angles = np.array([0, 0, xyz_dxdydz_rz[6]], dtype=np.float32)
        lidar_bbox_color = np.array(colors['Green'], dtype=np.float32)
        
        # Create a dictionary to store the lidar bounding box information
        label['lidar_bbox'] = {
            'lidar_xyz_center': lidar_xyz_center,
            'lidar_xyz_extent': lidar_xyz_extent,
            'lidar_xyz_euler_angles': lidar_xyz_euler_angles,
            'rgb_bbox_color': lidar_bbox_color,
            'predicted': False
        }
        
        output.append(label)
    
    return output