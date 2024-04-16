import open3d.visualization.gui as gui
from gui.logger_gui import Logger

import numpy as np
import os, shutil

def test_create_per_object_pcdet_dataset():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'},
                'data': {'path': './test_output'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict

    # import the function
    func = __import__('algo.post', fromlist=['create_per_object_pcdet_dataset']).create_per_object_pcdet_dataset

    # create dummy data
    point_cloud = (np.random.rand(10000, 4) - 0.5) * 10
    point_cloud[:, 3] = 1
    data_dict['current_point_cloud_numpy'] = point_cloud
    
    # run as it is running for bulk data
    for i in range(10):
        # create dummy label
        data_dict['current_label_list'] = [
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [1, 1, 1], 'lidar_xyz_euler_angles': [0, 0, 1]}},
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [2, 1, 0.5], 'lidar_xyz_euler_angles': [0, 0, 1]}},
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [1, 2, 0.5], 'lidar_xyz_euler_angles': [0, 0, 1]}},
        ]
        data_dict['current_label_path'] = str(i).zfill(4) + '.txt'

        # run the function
        func(data_dict, cfg_dict)

    # check if the output directories are created
    assert os.path.exists(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'per_object_pcdet_dataset', 'point_cloud'))
    assert os.path.exists(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'per_object_pcdet_dataset', 'label'))

    # count the number of files in the output directories
    point_cloud_files = os.listdir(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'per_object_pcdet_dataset', 'point_cloud'))
    label_files = os.listdir(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'per_object_pcdet_dataset', 'label'))
    assert len(point_cloud_files) == 30 # 3 labels for each of the 10 point clouds
    assert len(label_files) == 30 # 3 labels for each of the 10 point clouds
    
    # delete the output directories
    shutil.rmtree(os.path.join(cfg_dict['data']['path']))

def test_create_pcdet_dataset():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'},
                'data': {'path': './test_output'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict

    # import the function
    func = __import__('algo.post', fromlist=['create_pcdet_dataset']).create_pcdet_dataset

    # create dummy data
    point_cloud = (np.random.rand(10000, 4) - 0.5) * 10
    point_cloud[:, 3] = 1
    data_dict['current_point_cloud_numpy'] = point_cloud
    
    # run as it is running for bulk data
    for i in range(10):
        # create dummy label
        data_dict['current_label_list'] = [
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [1, 1, 1], 'lidar_xyz_euler_angles': [0, 0, 1]}},
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [2, 1, 0.5], 'lidar_xyz_euler_angles': [0, 0, 1]}},
            {'lidar_bbox': {'lidar_xyz_center': (np.random.rand(3)-0.5) * 5, 'lidar_xyz_extent': [1, 2, 0.5], 'lidar_xyz_euler_angles': [0, 0, 1]}},
        ]
        data_dict['current_label_path'] = str(i).zfill(4) + '.txt'

        # run the function
        func(data_dict, cfg_dict)

    # check if the output directories are created
    assert os.path.exists(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'pcdet_dataset', 'point_cloud'))
    assert os.path.exists(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'pcdet_dataset', 'label'))

    # count the number of files in the output directories
    point_cloud_files = os.listdir(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'pcdet_dataset', 'point_cloud'))
    label_files = os.listdir(os.path.join(cfg_dict['data']['path'], 'output', 'post', 'pcdet_dataset', 'label'))
    assert len(point_cloud_files) == 10 # input point clouds = output point clouds
    assert len(label_files) == 10 # each point cloud has one label file containing 3 labels
    
    # delete the output directories
    shutil.rmtree(os.path.join(cfg_dict['data']['path']))