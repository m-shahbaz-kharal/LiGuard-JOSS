import os
import numpy as np
import json

calib_file_extension = '.json'

def Handler(calib_path: str):
    """
    Loads calibration data from a file and returns a dictionary containing the calibration parameters.

    Args:
        calib_path (str): The path to the calibration file.

    Returns:
        dict: A dictionary containing the calibration parameters.

    Raises:
        None

    """

    if os.path.exists(calib_path) == False: return None
    
    calib = {}

    # Read the calibration file and populate the calib dictionary
    with open(calib_path, 'r') as f: calib = json.load(f)
    extrinsic_matrix  = np.reshape(calib['extrinsic'], [4,4]) # Tr_velo_to_cam
    intrinsic_matrix  = np.reshape(calib['intrinsic'], [3,3]) # P2
    
    # make sure the shapes and keys are correct
    calib['P2'] = intrinsic_matrix # 3x3
    calib['P2'] = np.hstack((calib['P2'], np.array([[0], [0], [0]], dtype=np.float32))) # 3x4
    calib['R0_rect'] = np.eye(4, dtype=np.float32)
    calib['Tr_velo_to_cam'] = extrinsic_matrix

    return calib