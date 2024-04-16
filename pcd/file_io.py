import open3d as o3d
import numpy as np
import os
import glob
import time
import threading

supported_file_types = ['.bin', '.npy', '.ply', '.pcd']

import os
import glob
import threading
import time
import numpy as np
import open3d as o3d

class FileIO:
    """
    Class for reading point cloud data from files.

    Args:
        cfg (dict): Configuration dictionary containing the path and file type information.

    Attributes:
        cfg (dict): Configuration dictionary containing the path and file type information.
        pcd_dir (str): Directory path where the point cloud files are located.
        pcd_type (str): File extension of the point cloud files.
        pcd_count (int): Number of point cloud files to read.
        files_basenames (list): List of file basenames (without extension) of the point cloud files.
        reader (function): Function to read the point cloud file based on its type.
        data_lock (threading.Lock): Lock for thread-safe access to the data list.
        data (list): List of tuples containing the absolute file path and the loaded point cloud data.
        stop (threading.Event): Event to stop the asynchronous reading thread.

    """

    def __init__(self, cfg: dict):
        self.cfg = cfg     
        self.pcd_dir = os.path.join(cfg['data']['path'], cfg['data']['lidar_subdir'])
        self.pcd_type = cfg['data']['lidar']['pcd_type']
        self.pcd_count = cfg['data']['size']
        files = glob.glob(os.path.join(self.pcd_dir, '*' + self.pcd_type))
        file_basenames = [os.path.splitext(os.path.basename(file))[0] for file in files]
        # Sort the file basenames based on the numerical part
        file_basenames.sort(key=lambda file_name: int(''.join(filter(str.isdigit, file_name))))
        self.files_basenames = file_basenames[:self.pcd_count]
        
        # Check if the file type is supported
        if self.pcd_type not in supported_file_types:
            raise NotImplementedError("File type not supported. Supported file types: " + ', '.join(supported_file_types) + ".")
        self.reader = getattr(self, '__read_' + self.pcd_type[1:] + '__')
        
        self.data_lock = threading.Lock()
        self.data = []
        self.stop = threading.Event()
        # Start the asynchronous reading thread
        threading.Thread(target=self.__async_read_fn__).start()
    
    def __read_bin__(self, file_abs_path: str):
        """
        Read point cloud data from a binary file.

        Args:
            file_abs_path (str): Absolute path of the binary file.

        Returns:
            numpy.ndarray: Loaded point cloud data as a numpy array.

        """
        return np.fromfile(file_abs_path, dtype=np.float32).reshape(-1,4)

    def __read_npy__(self, file_abs_path: str):
        """
        Read point cloud data from a numpy file.

        Args:
            file_abs_path (str): Absolute path of the numpy file.

        Returns:
            numpy.ndarray: Loaded point cloud data as a numpy array.

        """
        return np.load(file_abs_path)

    def __read_ply__(self, file_abs_path: str):
        """
        Read point cloud data from a PLY file.

        Args:
            file_abs_path (str): Absolute path of the PLY file.

        Returns:
            numpy.ndarray: Loaded point cloud data as a numpy array.

        """
        points = np.asarray(o3d.io.read_point_cloud(file_abs_path).points, dtype=np.float32)
        points = np.hstack((points, np.ones((points.shape[0], 1), dtype=np.float32)))
        return points
    
    def __read_pcd__(self, file_abs_path: str):
        """
        Read point cloud data from a PCD file.

        Args:
            file_abs_path (str): Absolute path of the PCD file.

        Returns:
            numpy.ndarray: Loaded point cloud data as a numpy array.

        """
        points = np.asarray(o3d.io.read_point_cloud(file_abs_path).points, dtype=np.float32)
        points = np.hstack((points, np.ones((points.shape[0], 1), dtype=np.float32)))
        return points
        
    def get_abs_path(self, idx: int):
        """
        Get the absolute file path of a point cloud file.

        Args:
            idx (int): Index of the file basename in the list.

        Returns:
            str: Absolute file path of the point cloud file.

        """
        return os.path.join(self.pcd_dir, self.files_basenames[idx] + self.pcd_type)
        
    def __async_read_fn__(self):
        """
        Asynchronous function to read point cloud files in the background.

        """
        for idx in range(len(self.files_basenames)):
            if self.stop.is_set():
                break
            file_abs_path = self.get_abs_path(idx)
            pcd_np = self.reader(file_abs_path)
            with self.data_lock:
                self.data.append((file_abs_path, pcd_np))
            time.sleep(self.cfg['threads']['io_sleep'])
        
    def __len__(self):
        """
        Get the number of point cloud files.

        Returns:
            int: Number of point cloud files.

        """
        return len(self.files_basenames)
    
    def __getitem__(self, idx):
        """
        Get the point cloud data at the specified index.

        Args:
            idx (int): Index of the point cloud file.

        Returns:
            tuple: Tuple containing the absolute file path and the loaded point cloud data.

        """
        try:
            with self.data_lock:
                return self.data[idx]
        except:
            file_abs_path = self.get_abs_path(idx)
            return (file_abs_path, self.reader(file_abs_path))
        
    def close(self):
        """
        Stop the asynchronous reading thread.

        """
        self.stop.set()