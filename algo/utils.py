'''
This file contains utility functions that are used by the algorithms in the pipeline.
'''

from gui.logger_gui import Logger

def gather_point_clouds(data_dict: dict, cfg_dict: dict, key: str, count: int, global_index_key: str = None):
    """
    Gathers point clouds until a specified count is reached.
    
    Args:
        data_dict (dict): The dictionary containing the data.
        cfg_dict (dict): The dictionary containing the configuration data.
        key (str): The key to store the gathered point clouds in the data dictionary.
        count (int): The desired count of point clouds to gather.
        global_index_key (str, optional): The key to store the indices of the gathered frames in the data dictionary. Defaults to None.
    
    Returns:
        bool: True if the gathering is completed, False otherwise.
    """
    logger: Logger = data_dict['logger']
    
    gathering_not_started = key not in data_dict
    if gathering_not_started:
        data_dict[key] = []
        logger.log(f'[algo->utils.py->gather_point_clouds[{key}]]: Gathering {count} point clouds', Logger.INFO)
    
    if global_index_key is None:
        global_index_key = f'{key}_gathered_frames_indices'
    if global_index_key not in data_dict:
        data_dict[global_index_key] = []
    
    # Check if gathering is completed
    gathering_completed = len(data_dict[key]) >= count
    point_cloud_is_present = 'current_point_cloud_numpy' in data_dict
    point_cloud_is_novel = data_dict['current_frame_index'] not in data_dict[global_index_key]
    
    # Gather the point cloud if gathering is not completed and the point cloud is present and novel
    if not gathering_completed and point_cloud_is_present and point_cloud_is_novel:
        data_dict[key].append(data_dict['current_point_cloud_numpy'])
        data_dict[global_index_key].append(data_dict['current_frame_index'])
    
    gathering_completed = len(data_dict[key]) >= count
    return gathering_completed


def combine_gathers(data_dict: dict, cfg_dict: dict, key: str, gather_keys: list):
    """
    Combines multiple gathers into a single gather.
    
    Args:
        data_dict (dict): The dictionary containing the data.
        cfg_dict (dict): The dictionary containing the configuration data.
        key (str): The key to store the combined gather in the data dictionary.
        gather_keys (list): The keys of the gathers to combine.
    """
    # Get logger object from data_dict
    logger: Logger = data_dict['logger']

    # Check if combining has started
    combining_not_started = key not in data_dict
    if combining_not_started:
        data_dict[key] = []
        logger.log(f'[algo->utils.py->combine_gathers[{key}]]: Combining {len(gather_keys)} gathers', Logger.INFO)
        for gather_key in gather_keys:
            data_dict[key].extend(data_dict[gather_key])


def skip_frames(data_dict: dict, cfg_dict: dict, key: str, skip: int, global_index_key: str = None):
    """
    Skips frames until a specified count is reached.
    
    Args:
        data_dict (dict): The dictionary containing the data.
        cfg_dict (dict): The dictionary containing the configuration data.
        key (str): The key to store the skipped frames count in the data dictionary.
        skip (int): The desired count of frames to skip.
        global_index_key (str, optional): The key to store the indices of the skipped frames in the data dictionary. Defaults to None.
    
    Returns:
        bool: True if the skipping is completed, False otherwise.
    """
    # Get logger object from data_dict
    logger: Logger = data_dict['logger']

    # Check if skipping has started
    skipping_not_started = key not in data_dict
    if skipping_not_started:
        data_dict[key] = 0
        logger.log(f'[algo->utils.py->skip_frames[{key}]]: Skipping {skip} frames', Logger.INFO)
    
    if global_index_key is None:
        global_index_key = f'{key}_skipped_frames_indices'
    if global_index_key not in data_dict:
        data_dict[global_index_key] = []
    
    # Check if skipping is completed
    skipping_completed = data_dict[key] >= skip
    point_cloud_is_present = 'current_point_cloud_numpy' in data_dict
    point_cloud_is_novel = data_dict['current_frame_index'] not in data_dict[global_index_key]
    
    # Skip the frame if skipping is not completed and the point cloud is present and novel
    if not skipping_completed and point_cloud_is_present and point_cloud_is_novel:
        data_dict[key] += 1
        data_dict[global_index_key].append(data_dict['current_frame_index'])
        
    skipping_completed = data_dict[key] >= skip
    return skipping_completed