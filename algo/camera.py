# contains the image processing algorithms

import numpy as np
from gui.logger_gui import Logger

def project_point_cloud_points(data_dict: dict, cfg_dict: dict):
    """
    Projects the points from a point cloud onto an image.

    Args:
        data_dict (dict): A dictionary containing the required data.
        cfg_dict (dict): A dictionary containing configuration parameters.

    Returns:
        None
    """
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->camera.py->project_point_cloud_points][CRITICAL]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return
    
    # Check if required data is present in data_dict
    if "current_point_cloud_numpy" not in data_dict:
        logger.log('[algo->camera.py->project_point_cloud_points]: current_point_cloud_numpy not found in data_dict', Logger.ERROR)
        return
    
    if "current_image_numpy" not in data_dict:
        logger.log('[alog->camera.py->project_point_cloud_points]: current_image_numpy not found in data_dict', Logger.ERROR)
        return
    
    if 'current_calib_data' not in data_dict:
        logger.log('[algo->camera.pyproject_point_cloud_points]: current_calib_data not found in data_dict', Logger.ERROR)
        return
    
    # Extract required calibration data
    Tr_velo_to_cam = data_dict['current_calib_data']['Tr_velo_to_cam']
    
    if 'R0_rect' in data_dict['current_calib_data']:
        R0_rect = data_dict['current_calib_data']['R0_rect']
    else:
        R0_rect = np.eye(4,4)
    
    P2 = data_dict['current_calib_data']['P2']
    
    # Convert lidar coordinates to homogeneous coordinates
    lidar_coords_Nx4 = np.hstack((data_dict['current_point_cloud_numpy'][:,:3], np.ones((data_dict['current_point_cloud_numpy'].shape[0], 1))))
    
    # Project lidar points onto the image plane
    pixel_coords = P2 @ R0_rect @ Tr_velo_to_cam @ lidar_coords_Nx4.T
    
    # Compute lidar depths
    lidar_depths = np.linalg.norm(lidar_coords_Nx4[:, :3], axis=1)
    
    # Filter out points that are behind the camera
    front_pixel_coords = pixel_coords[:, pixel_coords[2] > 0]
    front_lidar_depths = lidar_depths[pixel_coords[2] > 0]
    
    # Normalize pixel coordinates
    front_pixel_coords = front_pixel_coords[:2] / front_pixel_coords[2]
    front_pixel_coords = front_pixel_coords.T
    
    # Adjust lidar depths for visualization
    front_lidar_depths = front_lidar_depths * 6.0
    front_lidar_depths = 255.0 - np.clip(front_lidar_depths, 0, 255)
    
    # Convert pixel coordinates and lidar depths to the appropriate data types
    front_pixel_coords = front_pixel_coords.astype(int)
    front_lidar_depths = front_lidar_depths.astype(np.uint8)
    
    # Filter out coordinates that are outside the image boundaries
    valid_coords = (front_pixel_coords[:, 0] >= 0) & (front_pixel_coords[:, 0] < data_dict['current_image_numpy'].shape[1]) & (front_pixel_coords[:, 1] >= 0) & (front_pixel_coords[:, 1] < data_dict['current_image_numpy'].shape[0])
    
    # Select valid pixel coordinates and corresponding lidar depths
    pixel_coords_valid = front_pixel_coords[valid_coords]
    pixel_depths_valid = front_lidar_depths[valid_coords]
    
    # Update the image with the projected lidar points
    data_dict['current_image_numpy'][pixel_coords_valid[:, 1], pixel_coords_valid[:, 0]] = np.column_stack((pixel_depths_valid, np.zeros_like(pixel_depths_valid), np.zeros_like(pixel_depths_valid)))
