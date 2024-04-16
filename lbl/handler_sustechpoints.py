import os
import numpy as np
import json

colors = {
    "Car":            (0  ,255,0  ),#'#00ff00',
    "Van":            (0  ,255,0  ),#'#00ff00',
    "Bus":            (0  ,255,255),#'#ffff00', 
    "Pedestrian":     (0  ,0  ,255),#'#ff0000',
    "Rider":          (0  ,136,255),#'#ff8800',
    "Cyclist":        (0  ,136,255),#'#ff8800',
    "Bicycle":        (0  ,255,136),#'#88ff00',
    "BicycleGroup":   (0  ,255,136),#'#88ff00',
    "Motor":          (0  ,176,176),#'#aaaa00',
    "Truck":          (255,255,0  ),#'#00ffff',
    "Tram":           (255,255,0  ),#'#00ffff',
    "Animal":         (255,176,0  ),#'#00aaff',
    "Misc":           (136,136,0  ),#'#008888',
    "Unknown":        (136,136,0  ),#'#008888',
}
label_file_extension = '.json'

import os
import json
import numpy as np

def Handler(label_path: str, calib_data: dict):
    """
    Process the label file and return a list of labels.

    Args:
        label_path (str): The path to the label file.
        calib_data (dict): Calibration data.

    Returns:
        list: A list of labels.

    """
    output = []
        
    # Read label file
    if os.path.exists(label_path) == False:
        return output
    
    with open(label_path, 'r') as f:
        lbls = json.load(f)
    
    for item in lbls:
        # Extract label information
        annotator = item['annotator'] if 'annotator' in item else 'Unknown'
        obj_id = int(item['obj_id'])
        obj_type = item['obj_type']
        psr = item['psr']
        psr_position_xyz = np.array([psr['position']['x'], psr['position']['y'], psr['position']['z']], dtype=np.float32)
        psr_rotation_xyz = np.array([psr['rotation']['x'], psr['rotation']['y'], psr['rotation']['z']], dtype=np.float32)
        psr_scale_xyz = np.array([psr['scale']['x'], psr['scale']['y'], psr['scale']['z']], dtype=np.float32)
        
        # Create a dictionary to store the label information
        label = {}
        label['annotator'] = annotator
        label['obj_id'] = obj_id
        label['obj_type'] = obj_type
        label['psr'] = psr
                  
        lidar_xyz_center = psr_position_xyz.copy()
        lidar_xyz_extent = psr_scale_xyz.copy()
        lidar_xyz_euler_angles = psr_rotation_xyz.copy()

        # create color for the bounding box
        if obj_type in colors:
            lidar_bbox_color = np.array([i / 255.0 for i in colors[obj_type]], dtype=np.float32)
        else:
            lidar_bbox_color = np.array([0, 0, 0], dtype=np.float32)
        
        # Create a dictionary to store the lidar bounding box information
        label['lidar_bbox'] = {
            'lidar_xyz_center': lidar_xyz_center,
            'lidar_xyz_extent': lidar_xyz_extent,
            'lidar_xyz_euler_angles': lidar_xyz_euler_angles,
            'rgb_bbox_color': lidar_bbox_color,
            'predicted': False
        }
        
        if obj_type in colors:
            camera_bbox_color = np.array(colors[obj_type], dtype=np.uint8)
        else:
            camera_bbox_color = np.array([0, 0, 0], dtype=np.uint8)
        
        # Create a dictionary to store the camera bounding box information
        label['camera_bbox'] = {
            'lidar_xyz_center': lidar_xyz_center,
            'lidar_xyz_extent': lidar_xyz_extent,
            'lidar_xyz_euler_angles': lidar_xyz_euler_angles,
            'rgb_bbox_color': camera_bbox_color,
            'predicted': False
        }
        
        # Append the label to the output list
        output.append(label)
    
    return output