import open3d.visualization.gui as gui
from gui.logger_gui import Logger

def test_remove_out_of_bound_labels():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict
    
    # import the function
    func = __import__('algo.label', fromlist=['remove_out_of_bound_labels']).remove_out_of_bound_labels

    # crop bound
    cfg_dict['proc'] = {'lidar': {'crop': {'min_xyz': [0, 0, 0], 'max_xyz': [10, 10, 10]}}}
    
    # create dummy data
    data_dict['current_label_list'] = []

    # add a label that is out of bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [11, 11, 11]}})
    # add anotehr label that is out of bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [-1, -1, -1]}})
    # add another label that is out of bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [5, 5, 11]}})
    # add another label that is out of bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [5, 11, 5]}})
    # add another label that is out of bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [11, 5, 5]}})
    # add a label that is within bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [5, 5, 5]}})
    # add another label that is within bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [0, 0, 0]}})
    # add another label that is within bound
    data_dict['current_label_list'].append({'lidar_bbox': {'lidar_xyz_center': [10, 10, 10]}})

    # run the function
    func(data_dict, cfg_dict)

    # check if the label list is updated
    assert len(data_dict['current_label_list']) == 3, f'Expected 3 labels, got {len(data_dict["current_label_list"])}'

