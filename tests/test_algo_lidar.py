import open3d.visualization.gui as gui
from gui.logger_gui import Logger

import numpy as np

def test_crop():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict
    
    # import the function
    func = __import__('algo.lidar', fromlist=['crop']).crop

    # crop bound
    cfg_dict['proc'] = {'lidar': {'crop': {'min_xyz': [0, 0, 0], 'max_xyz': [10, 10, 10]}}}

    # create dummy data
    data_dict['current_point_cloud_numpy'] = np.zeros((8, 3))

    # add points that are out of bound
    data_dict['current_point_cloud_numpy'][0] = [11, 11, 11]
    data_dict['current_point_cloud_numpy'][1] = [-1, -1, -1]
    data_dict['current_point_cloud_numpy'][2] = [5, 5, 11]
    data_dict['current_point_cloud_numpy'][3] = [5, 11, 5]
    data_dict['current_point_cloud_numpy'][4] = [11, 5, 5]
    # add points that are within bound
    data_dict['current_point_cloud_numpy'][5] = [5, 5, 5]
    data_dict['current_point_cloud_numpy'][6] = [0, 0, 0]
    data_dict['current_point_cloud_numpy'][7] = [10, 10, 10]

    # run the function
    func(data_dict, cfg_dict)

    # check if the point cloud is updated
    assert data_dict['current_point_cloud_numpy'].shape[0] == 3, f'Expected 3 points, got {data_dict["current_point_cloud_numpy"].shape[0]}'

def test_project_image_pixel_colors():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict
    
    # import the function
    func = __import__('algo.lidar', fromlist=['project_image_pixel_colors']).project_image_pixel_colors
    
    # create dummy calibration data
    P2 = np.eye(3, 4)
    R0_rect = np.eye(4)
    Tr_velo_to_cam = np.eye(4)
    data_dict['current_calib_data'] = {'P2': P2, 'R0_rect': R0_rect, 'Tr_velo_to_cam': Tr_velo_to_cam}
    
    # Create dummy point cloud
    point_cloud = np.zeros((100, 3))

    # tests
    # all points lie in the x-y plane, are in image boundsm and are in front of the camera
    data_dict['current_point_cloud_point_colors'] = np.zeros((100, 3), dtype=np.float32)
    data_dict['current_image_numpy'] = np.zeros((100, 100, 3), dtype=np.uint8)
    # make the image green
    data_dict['current_image_numpy'][:, :, 1] = 255
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    z = 1.
    x, y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    point_cloud[:, 0] = x
    point_cloud[:, 1] = y
    point_cloud[:, 2] = z
    data_dict['current_point_cloud_numpy'] = point_cloud

    # run the function
    func(data_dict, cfg_dict)

    # check if all the points in the point cloud are green
    assert np.all(data_dict['current_point_cloud_point_colors'] == [0,1,0]), 'All points in the point cloud should be green'

    # 19 points lie outside the image plane
    data_dict['current_point_cloud_point_colors'] = np.zeros((100, 3), dtype=np.float32)
    data_dict['current_image_numpy'] = np.zeros((100, 100, 3), dtype=np.uint8)
    # make the image green
    data_dict['current_image_numpy'][:, :, 1] = 255
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 900]
    y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 900]
    z = 1.0
    x, y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    point_cloud[:, 0] = x
    point_cloud[:, 1] = y
    point_cloud[:, 2] = z
    data_dict['current_point_cloud_numpy'] = point_cloud

    # run the function
    func(data_dict, cfg_dict)

    # count the number of green points
    number_of_green_points = np.sum(np.all(data_dict['current_point_cloud_point_colors'] == [0,1,0], axis=1))
    assert number_of_green_points == 81, f'Expected 81 green points, got {number_of_green_points}'


