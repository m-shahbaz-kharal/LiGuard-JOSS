import os
import numpy as np

colors = {
    'Car': [0, 1, 0],
    'Van': [0, 1, 0],
    'Truck': [0, 1, 0],
    'Pedestrian': [1, 0, 0],
    'Person_sitting': [1, 0, 0],
    'Cyclist': [0, 0, 1],
    'Tram': [1, 1, 0],
    'Misc': [1, 1, 0],
    'DontCare': [1, 1, 1]
}
label_file_extension = '.txt'

import os
import numpy as np

def Handler(label_path: str, calib_data: dict):
    """
    Process the label file and generate a list of labels.

    Args:
        label_path (str): Path to the label file.
        calib_data (dict): Calibration data.

    Returns:
        list: List of labels.

    """
    output = []

    if calib_data is None:
        return output

    transform_from_lidar_to_image_0 = calib_data['Tr_velo_to_cam']
    transform_from_image_0_to_lidar = np.linalg.inv(transform_from_lidar_to_image_0)
    
    # Read label file
    if not os.path.exists(label_path):
        return output
    with open(label_path, 'r') as f:
        lbls = f.readlines()
    
    for line in lbls:
        parts = line.strip().split(' ')
        obj_class = parts[0]  # Object class [Car, Van, Truck, Pedestrian, Person_sitting, Cyclist, Tram, Misc, DontCare]
        truncation = float(parts[1])  # Truncated pixel ratio [0..1]
        occlusion = int(parts[2])  # 0: fully visible, 1: partly occluded, 2: fully occluded, 3: unknown
        alpha = float(parts[3])  # Object observation angle [-pi..pi]
        left, top, right, bottom = np.array([float(x) for x in parts[4:8]], dtype=np.float32)  # 0-based 2D bounding box of object in the image
        height, width, length = np.array([float(x) for x in parts[8:11]], dtype=np.float32)  # Height, width, length in meters
        image_0_xyz = np.array([float(x) for x in parts[11:14]], dtype=np.float32)  # Location of object center in camera coordinates
        image_0_ry = float(parts[14])  # Rotation around Y-axis in camera coordinates [-pi..pi]
        
        label = dict()
        label['class'] = obj_class
        label['truncation'] = truncation
        label['occlusion'] = occlusion
        label['alpha'] = alpha
        label['image_0_bbox2d'] = [left, top, right, bottom]
        label['obj_height'] = height
        label['obj_width'] = width
        label['obj_length'] = length
        label['image_0_xyz'] = image_0_xyz
        label['image_0_ry'] = image_0_ry
        
        # project to lidar coordinates
        lidar_xyz_center = transform_from_image_0_to_lidar @ np.append(image_0_xyz, 1).reshape(4, 1)
        lidar_xyz_center = lidar_xyz_center.T[0]
        lidar_xyz_center = lidar_xyz_center[:3]
        # Adjust the height of the bounding box since the origin of the lidar coordinates is at the bottom of the vehicle
        lidar_xyz_center[2] += height / 2.0
        # w l h -> x y z
        lidar_xyz_extent = np.array([width, length, height], dtype=np.float32)
        lidar_xyz_euler_angles = np.array([0, 0, -image_0_ry], dtype=np.float32)
        lidar_bbox_color = np.array(colors[obj_class], dtype=np.float32)
        
        # visualzer expect lidar_bbox to be present in order to visualize the bounding boxes, so we add them here
        label['lidar_bbox'] = {'lidar_xyz_center': lidar_xyz_center, 'lidar_xyz_extent': lidar_xyz_extent, 'lidar_xyz_euler_angles': lidar_xyz_euler_angles, 'rgb_bbox_color': lidar_bbox_color, 'predicted': False}
        
        # camera colors are in the range 0-255
        camera_bbox_color = np.array([i * 255.0 for i in colors[obj_class]], dtype=np.uint8)
        
        # visualzer expect camera_bbox to be present in order to visualize the bounding boxes, so we add them here
        label['camera_bbox'] = {'lidar_xyz_center': lidar_xyz_center, 'lidar_xyz_extent': lidar_xyz_extent, 'lidar_xyz_euler_angles': lidar_xyz_euler_angles, 'rgb_bbox_color': camera_bbox_color, 'predicted': False}
        
        output.append(label)
    
    return output