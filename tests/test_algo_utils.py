import open3d.visualization.gui as gui
from gui.logger_gui import Logger

import numpy as np

def test_gather_skip_gather_combine():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict

    # import the function
    gather = __import__('algo.utils', fromlist=['gather_point_clouds']).gather_point_clouds
    skip = __import__('algo.utils', fromlist=['skip_frames']).skip_frames
    combine = __import__('algo.utils', fromlist=['combine_gathers']).combine_gathers

    for i in range(10):
        data_dict['current_point_cloud_numpy'] = np.random.rand(1000, 4)
        data_dict['current_frame_index'] = i

        done = gather(data_dict, cfg_dict, 'set_1', 3, 'global_gather')
        done = gather(data_dict, cfg_dict, 'set_1', 3, 'global_gather')
        if not done: continue
        done = skip(data_dict, cfg_dict, 'skip_1', 2, 'global_skip')
        done = skip(data_dict, cfg_dict, 'skip_1', 2, 'global_skip')
        if not done: continue
        done = gather(data_dict, cfg_dict, 'set_2', 3, 'global_gather')
        done = gather(data_dict, cfg_dict, 'set_2', 3, 'global_gather')
        if not done: continue
        done = skip(data_dict, cfg_dict, 'skip_2', 2, 'global_skip')
        done = skip(data_dict, cfg_dict, 'skip_2', 2, 'global_skip')
    
    assert len(data_dict['global_gather']) == 6 # no duplicates, 3 for set_1 and 3 for set_2, repeated calls should not add duplicates
    assert len(data_dict['global_skip']) == 4 # 2 for skip_1 and 2 for skip_2
    combine(data_dict, cfg_dict, 'combined', ['set_1', 'set_2'])
    assert len(data_dict['combined']) == 6 # 3 for set_1 and 3 for set_2
