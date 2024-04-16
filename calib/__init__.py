"""
The calib package manages calibration file handlers for reading calibration files. The `file_io.py` module should not be modified except for contributions to the framework application logic.

### Creating a New Calibration File Handler:

To create a new calibration file handler:

1. Create a new Python file named `handler_<clb_type>.py` in the `calib` directory.
2. Replace `<clb_type>` with the specific type of calibration file (e.g., `lidar`, `camera`, etc.).
3. The `clb_type` is passed from `config.yml` under `data:calib:clb_type` and is used to select the appropriate handler.

### Handler File Structure:

The handler file should contain the following elements:

```python
# handler_<clb_type>.py

import os

# Extension for calibration files handled by this handler
calib_file_extension = '.txt'

def Handler(calib_path: str):
    '''
    Loads calibration data from the specified file path and returns it as a dictionary containing P2, R0_rect, and Tr_velo_to_cam.

    Args:
        calib_path (str): The path to the calibration file.

    Returns:
        dict: A dictionary containing the calibration data.
    '''
    

    # Check if the calibration file exists
    if not os.path.exists(calib_path):
        return None
    
    calib = {}
    
    # Read the calibration file and populate the calib dictionary
    with open(calib_path) as f:
        pass  # read the calibration file and populate the calib dictionary

    # Reshape matrices to required shapes
    calib['P2'] = calib['P2'].reshape(3, 4)  # P2 must be reshaped to 3x4
    calib['R0_rect'] = calib['R0_rect'].reshape(3, 3)  # R0_rect must be reshaped to 3x3
    calib['Tr_velo_to_cam'] = calib['Tr_velo_to_cam'].reshape(3, 4)  # Tr_velo_to_cam must be reshaped to 3x4

    return calib
```

"""
