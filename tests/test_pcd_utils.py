import numpy as np

def test_create_pcd():
    from pcd.utils import create_pcd
    # Test case 1: Empty array
    points = np.array([])
    pcd = create_pcd(points)
    assert len(pcd.points) == 0

    # Test case 2: Single point
    points = np.array([[1, 2, 3]])
    pcd = create_pcd(points)
    assert len(pcd.points) == 1
    assert np.allclose(pcd.points[0], [1, 2, 3])

    # Test case 3: Multiple points
    points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    pcd = create_pcd(points)
    assert len(pcd.points) == 3
    assert np.allclose(pcd.points[0], [1, 2, 3])
    assert np.allclose(pcd.points[1], [4, 5, 6])
    assert np.allclose(pcd.points[2], [7, 8, 9])

def test_update_pcd():
    import open3d as o3d
    from pcd.utils import update_pcd
    # Test case 1: Empty array
    points = np.array([])
    pcd = update_pcd(o3d.geometry.PointCloud(), points)
    assert len(pcd.points) == 0

    # Test case 2: Single point
    points = np.array([[1, 2, 3]])
    pcd = update_pcd(o3d.geometry.PointCloud(), points)
    assert len(pcd.points) == 1
    assert np.allclose(pcd.points[0], [1, 2, 3])

    # Test case 3: Multiple points
    points = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    pcd = update_pcd(o3d.geometry.PointCloud(), points)
    assert len(pcd.points) == 3
    assert np.allclose(pcd.points[0], [1, 2, 3])
    assert np.allclose(pcd.points[1], [4, 5, 6])
    assert np.allclose(pcd.points[2], [7, 8, 9])

def test_get_fixed_sized_point_cloud():
    from pcd.utils import get_fixed_sized_point_cloud
    # Test case 1: Empty array
    point_cloud = np.array([])
    number_of_points = 10
    fixed_sized_point_cloud = get_fixed_sized_point_cloud(point_cloud, number_of_points)
    assert fixed_sized_point_cloud.shape == (number_of_points, 3)

    # Test case 2: Fewer points
    point_cloud = np.array([[1, 2, 3], [4, 5, 6]])
    number_of_points = 10
    fixed_sized_point_cloud = get_fixed_sized_point_cloud(point_cloud, number_of_points)
    assert fixed_sized_point_cloud.shape == (number_of_points, 3)
    assert np.allclose(fixed_sized_point_cloud[:2], point_cloud)

    # Test case 3: More points
    point_cloud = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    number_of_points = 2
    fixed_sized_point_cloud = get_fixed_sized_point_cloud(point_cloud, number_of_points)
    assert fixed_sized_point_cloud.shape == (number_of_points, 3)
    assert np.allclose(fixed_sized_point_cloud, point_cloud[:number_of_points])