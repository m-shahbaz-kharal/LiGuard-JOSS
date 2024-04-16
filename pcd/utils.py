import open3d as o3d
import numpy as np

"""
The module utils.py contains utility functions for working with point clouds. If you think that a function can be reused in other parts of the framework, you can move it to the utils.py module.
"""

def create_pcd(points: np.ndarray) -> o3d.geometry.PointCloud:
    """
    Create a PointCloud object from a numpy array of points.

    Args:
        points (np.ndarray): Array of points with shape (N, 3).

    Returns:
        o3d.geometry.PointCloud: PointCloud object.

    """
    if points.size == 0: return o3d.geometry.PointCloud()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, 0:3])
    return pcd

def update_pcd(pcd: o3d.geometry.PointCloud, points: np.ndarray) -> o3d.geometry.PointCloud:
    """
    Update the points of a PointCloud object with a new set of points.

    Args:
        pcd (o3d.geometry.PointCloud): PointCloud object to update.
        points (np.ndarray): Array of points with shape (N, 3).

    Returns:
        o3d.geometry.PointCloud: Updated PointCloud object.

    """
    if points.size == 0: return pcd
    pcd.points = o3d.utility.Vector3dVector(points[:, 0:3])
    return pcd

def get_fixed_sized_point_cloud(point_cloud: np.ndarray, number_of_points: int) -> np.ndarray:
    """
    Get a fixed-sized point cloud by padding or cropping the input point cloud.

    Args:
        point_cloud (np.ndarray): Input point cloud with shape (N, 3).
        number_of_points (int): Desired number of points in the fixed-sized point cloud.

    Returns:
        np.ndarray: Fixed-sized point cloud with shape (number_of_points, 3).

    """
    # pad if less points
    if point_cloud.shape[0] == 0: point_cloud = np.zeros((number_of_points, 3))
    if point_cloud.shape[0] < number_of_points:
        point_cloud = np.pad(point_cloud, ((0, number_of_points - point_cloud.shape[0]), (0, 0)), mode='constant', constant_values=0)
    # crop if more points
    elif point_cloud.shape[0] > number_of_points:
        point_cloud = point_cloud[:number_of_points]
    return point_cloud