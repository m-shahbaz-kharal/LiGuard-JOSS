from inspect import isfunction

import open3d.visualization.gui as gui
from gui.logger_gui import Logger

def test_all_algo_validity():
    # create dummy configuration and data dictionaries
    cfg_dict = {'logging': {'level': 0, 'path': 'logs'}}
    data_dict = {}

    # create a logger object as it is required by some algorithms
    logger:Logger = Logger()
    logger.reset(cfg_dict)

    data_dict['logger'] = logger # add logger object to data_dict

    all_algo = [] # a list of all the algorithms under the algo directory

    # add algorithms from all the submodules
    # pre
    pre = __import__('algo.pre', fromlist=['*'])
    pre = [getattr(pre, algo) for algo in dir(pre) if isfunction(getattr(pre, algo))]
    all_algo.extend(pre)
    # lidar
    lidar = __import__('algo.lidar', fromlist=['*'])
    lidar = [getattr(lidar, algo) for algo in dir(lidar) if isfunction(getattr(lidar, algo))]
    all_algo.extend(lidar)
    # camera
    camera = __import__('algo.camera', fromlist=['*'])
    camera = [getattr(camera, algo) for algo in dir(camera) if isfunction(getattr(camera, algo))]
    all_algo.extend(camera)
    # calib
    calib = __import__('algo.calib', fromlist=['*'])
    calib = [getattr(calib, algo) for algo in dir(calib) if isfunction(getattr(calib, algo))]
    all_algo.extend(calib)
    # label
    label = __import__('algo.label', fromlist=['*'])
    label = [getattr(label, algo) for algo in dir(label) if isfunction(getattr(label, algo))]
    all_algo.extend(label)
    # post
    post = __import__('algo.post', fromlist=['*'])
    post = [getattr(post, algo) for algo in dir(post) if isfunction(getattr(post, algo))]
    all_algo.extend(post)

    # run each algorithm with the dummy data_dict and cfg_dict, they should crash, instead the error must logged and the function must return
    for algo in all_algo: algo(data_dict, cfg_dict)