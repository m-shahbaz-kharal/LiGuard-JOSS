"""
The lbl package comprises handlers for reading label files. The `file_io.py` module should not be modified except for contributions to the framework application logic.

### Creating a New Label File Handler:

To create a new label file handler:

1. Create a new Python file named `handler_<lbl_type>.py` in the `calib` directory.
2. Replace `<lbl_type>` with the specific type of label file (e.g., `kitti`, `coco`, etc.).
3. The `lbl_type` is passed from `config.yml` under `data:label:lbl_type` and is used to select the appropriate handler.

### Handler File Structure:

The `handler_<lbl_type>.py` file should contain the following elements:

- `colors`: A dictionary mapping object categories to colors.
- `label_file_extension`: A string specifying the file extension to look for.
- `Handler` function: Reads the label file and returns a list of dictionaries representing the labels.

```python
# hander_<lbl_type>.py

colors = {'Car': [1, 0, 0], 'Pedestrian': [0, 1, 0]}
label_file_extension = '.txt'

def Handler(label_path: str, calib_data: dict):
    '''
    Args:
        label_path (str): The path to the label file.
        calib_data (dict): Calibration data.

    Returns:
        list: A list of dictionaries representing the labels.
    '''
    import os
    
    output = []
    
    # Check if the label file exists
    if not os.path.exists(label_path):
        return output
    
    # Read the label file
    labels = []
    with open(label_path, 'r') as f:
        # read labels
    
    for label in labels:
        # extract label information
        
        # Example extraction:
        # lidar_xyz_center = ...
        # lidar_xyz_extent = ...
        # lidar_xyz_euler_angles = np.array([x, y, z], dtype=np.float32)
        # lidar_bbox_color = np.array(colors[obj_class], dtype=np.float32) # this is in 0-1 range
        # rgb_bbox_color = np.array(colors[obj_class], dtype=np.float32) * 255.0 # Convert to 0-255 range
        
        # Create a dictionary to store the lidar bounding box information
        label['lidar_bbox'] = {
            # 'lidar_xyz_center': lidar_xyz_center,
            # 'lidar_xyz_extent': lidar_xyz_extent,
            # 'lidar_xyz_euler_angles': lidar_xyz_euler_angles,
            # 'rgb_bbox_color': lidar_bbox_color,
            'predicted': False  # as the label is ground truth and is read from file
        }
        
        # Append the label to the output list
        output.append(label)
    
    return output  # return the list of dictionaries representing the labels
```

Ensure that the Handler function reads the label file specified by label_path and returns the label data as a list of dictionaries. Each dictionary should contain information about the label, including the bounding box coordinates and object class.
"""