# contains point-cloud processing algorithms

import numpy as np

from gui.logger_gui import Logger

def crop(data_dict: dict, cfg_dict: dict):
    """
    Crop the point cloud data based on the specified limits.

    Args:
        data_dict (dict): A dictionary containing the data.
        cfg_dict (dict): A dictionary containing the configuration parameters.

    Returns:
        None
    """
    
    # Get logger object from data_dict
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->lidar.py->crop]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return

    # Check if required data is present in data_dict
    if "current_point_cloud_numpy" not in data_dict:
        logger.log('[algo->lidar.py->crop]: current_point_cloud_numpy not found in data_dict', Logger.ERROR)
        return
    
    # Get point cloud and crop limits
    pcd = data_dict['current_point_cloud_numpy']
    min_xyz = cfg_dict['proc']['lidar']['crop']['min_xyz']
    max_xyz = cfg_dict['proc']['lidar']['crop']['max_xyz']
    
    # create conditions for cropping
    x_condition = np.logical_and(min_xyz[0] <= pcd[:, 0], pcd[:, 0] <= max_xyz[0])
    y_condition = np.logical_and(min_xyz[1] <= pcd[:, 1], pcd[:, 1] <= max_xyz[1])
    z_condition = np.logical_and(min_xyz[2] <= pcd[:, 2], pcd[:, 2] <= max_xyz[2])
    
    # Update the point cloud in data_dict
    data_dict['current_point_cloud_numpy'] = pcd[x_condition & y_condition & z_condition]
    data_dict['current_point_cloud_point_colors'] = np.ones((data_dict['current_point_cloud_numpy'].shape[0], 3), dtype=np.float32)
    
def project_image_pixel_colors(data_dict: dict, cfg_dict: dict):
    """
    Projects the colors of image pixels onto the point cloud.

    Args:
        data_dict (dict): A dictionary containing the required data for the operation.
        cfg_dict (dict): A dictionary containing configuration parameters.

    Returns:
        None
    """

    # Get logger object from data_dict
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->lidar.py->project_image_pixel_colors]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return
    
    # Check if required data is present in data_dict
    if "current_point_cloud_numpy" not in data_dict:
        logger.log('[algo->lidar.py->project_image_pixel_colors]: current_point_cloud_numpy not found in data_dict', Logger.ERROR)
        return
    if "current_image_numpy" not in data_dict:
        logger.log('[algo->lidar.py->project_image_pixel_colors]: current_image_numpy not found in data_dict', Logger.ERROR)
        return
    if "current_calib_data" not in data_dict:
        logger.log('[algo->lidar.py->project_image_pixel_colors]: current_calib_data not found in data_dict', Logger.ERROR)
        return
    
    # Extract required data
    img_np = data_dict['current_image_numpy']
    Tr_velo_to_cam = data_dict['current_calib_data']['Tr_velo_to_cam']
    R0_rect = data_dict['current_calib_data']['R0_rect']
    P2 = data_dict['current_calib_data']['P2']
    
    data_dict['current_point_cloud_point_colors'] = np.ones((data_dict['current_point_cloud_numpy'].shape[0], 3), dtype=np.float32) # N X 3(RGB)
    # Convert lidar coordinates to homogeneous coordinates
    lidar_coords_Nx4 = np.hstack((data_dict['current_point_cloud_numpy'][:,:3], np.ones((data_dict['current_point_cloud_numpy'].shape[0], 1))))
    
    # Project lidar points onto the image plane
    pixel_coords = P2 @ R0_rect @ Tr_velo_to_cam @ lidar_coords_Nx4.T
    
    # Normalize pixel coordinates
    normalized_pixel_coords_2d = pixel_coords[:2] / (pixel_coords[2] + 1e-8)
    normalized_pixel_coords_2d = normalized_pixel_coords_2d.T
    normalized_pixel_coords_2d = normalized_pixel_coords_2d.astype(int)
    
    # Filter out coordinates that are outside the image boundaries
    valid_coords = np.logical_and.reduce((pixel_coords[2,:] > 0, normalized_pixel_coords_2d[:, 0] >= 0, normalized_pixel_coords_2d[:, 0] < img_np.shape[1], normalized_pixel_coords_2d[:, 1] >= 0, normalized_pixel_coords_2d[:, 1] < img_np.shape[0]))
    # Update the point cloud colors in data_dict corresponding to the valid pixel coordinates
    data_dict['current_point_cloud_point_colors'][valid_coords] = img_np[normalized_pixel_coords_2d[valid_coords][:, 1], normalized_pixel_coords_2d[valid_coords][:, 0]] / 255.0
    