import cv2
import os
import glob
import time
import threading

class FileIO:
    """
    Class for reading and managing a collection of image files.

    Args:
        cfg (dict): Configuration dictionary containing the necessary parameters.

    Attributes:
        cfg (dict): Configuration dictionary.
        img_dir (str): Directory path where the image files are located.
        img_type (str): File extension of the image files.
        img_count (int): Number of image files to read.
        files_basenames (list): List of file basenames (without extension) of the image files.
        reader (function): Function to read an image file.
        data_lock (threading.Lock): Lock for thread-safe access to the data list.
        data (list): List of tuples containing the file absolute path and the image data.
        stop (threading.Event): Event to signal the thread to stop.

    Methods:
        __init__(self, cfg: dict): Initializes the FileIO object.
        __read_img__(self, file_abs_path: str): Reads an image file and returns the image data.
        get_abs_path(self, idx: int): Returns the absolute path of the image file at the given index.
        __async_read_fn__(self): Asynchronously reads the image files and populates the data list.
        __len__(self): Returns the number of image files.
        __getitem__(self, idx): Returns the image data and file absolute path at the given index.
        close(self): Stops the asynchronous reading process.

    """

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.img_dir = os.path.join(cfg['data']['path'], cfg['data']['camera_subdir'])
        self.img_type = cfg['data']['camera']['img_type']
        self.img_count = cfg['data']['size']
        files = glob.glob(os.path.join(self.img_dir, '*' + self.img_type))
        file_basenames = [os.path.splitext(os.path.basename(file))[0] for file in files]
        # Sort the file basenames based on the numerical part
        file_basenames.sort(key=lambda file_name: int(''.join(filter(str.isdigit, file_name))))
        self.files_basenames = file_basenames[:self.img_count]
        self.reader = self.__read_img__

        self.data_lock = threading.Lock()
        self.data = []
        self.stop = threading.Event()
        # Start the asynchronous reading thread
        threading.Thread(target=self.__async_read_fn__).start()

    def __read_img__(self, file_abs_path: str):
        """
        Reads an image file and returns the image data in RGB format.

        Args:
            file_abs_path (str): Absolute path of the image file.

        Returns:
            numpy.ndarray: Image data in RGB format.

        """
        img_bgr = cv2.imread(file_abs_path, cv2.IMREAD_UNCHANGED)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb

    def get_abs_path(self, idx: int):
        """
        Returns the absolute path of the image file at the given index.

        Args:
            idx (int): Index of the image file.

        Returns:
            str: Absolute path of the image file.

        """
        return os.path.join(self.img_dir, self.files_basenames[idx] + self.img_type)

    def __async_read_fn__(self):
        """
        Asynchronously reads the image files and populates the data list.

        """
        for idx in range(len(self.files_basenames)):
            if self.stop.is_set():
                break
            file_abs_path = self.get_abs_path(idx)
            pcd_np = self.reader(file_abs_path)
            with self.data_lock:
                # append the file absolute path and the image data to the data list
                self.data.append((file_abs_path, pcd_np))
            time.sleep(self.cfg['threads']['io_sleep'])

    def __len__(self):
        """
        Returns the number of image files.

        Returns:
            int: Number of image files.

        """
        return len(self.files_basenames)

    def __getitem__(self, idx):
        """
        Returns the image data and file absolute path at the given index.

        Args:
            idx (int): Index of the image file.

        Returns:
            tuple: Tuple containing the file absolute path and the image data.

        """
        try:
            with self.data_lock:
                return self.data[idx]
        except:
            file_abs_path = self.get_abs_path(idx)
            # return the file absolute path and the image data
            return (file_abs_path, self.reader(file_abs_path))

    def close(self):
        """
        Stops the asynchronous reading process.

        """
        self.stop.set()