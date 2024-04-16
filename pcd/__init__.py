"""
The pcd package comprises two types of handlers: (1) file handlers for reading point cloud files and (2) sensor handlers for capturing point cloud data from live LiDAR sensor feeds. The `file_io.py` and `sensor_io.py` modules should not be modified except for contributions to the framework application logic.

### Implementing a New Point Cloud Type:

To implement a new point cloud type:

1. Create a new function named `__read_<pcd_type>__` in the `file_io.py` file.
2. Replace `<pcd_type>` with the specific type of point cloud data (e.g., `velodyne`, `hdf5`, etc.).
3. The function should read the point cloud data from the binary file specified by the absolute path and return it as a NumPy array of shape `(N, 4)`, where `N` is the number of points and `4` represents the features `(x, y, z, intensity)`.

### Creating a New Sensor Stream Handler:

To create a new sensor stream handler to support a new LiDAR sensor:

1. Create a new Python file named `handler_<manufacturer>_<model>.py` in the `pcd` directory.
2. Replace `<manufacturer>` and `<model>` with the manufacturer and model of the LiDAR sensor.
3. The manufacturer and model are passed from `config.yml` under `sensors:lidar:manufacturer` and `sensors:lidar:model`, respectively, and are used to select the appropriate handler.

### Handler File Structure:

The `handler_<manufacturer>_<model>.py` file should contain a class named `Handler` with the following structure:

```python
# hander_<manufacturer>_<model>.py

class Handler:
    '''
    Args:
        cfg (dict): Configuration dictionary containing sensor information.

    Attributes:
        cfg (dict): Configuration dictionary containing sensor information.
        manufacturer (str): Manufacturer of the LiDAR sensor.
        model (str): Model of the LiDAR sensor.
        serial_no (str): Serial number of the LiDAR sensor.
        hostname (str): Hostname of the LiDAR sensor.
        reader (generator): Generator that yields point cloud data.

    Raises:
        Exception: If fails to connect to the LiDAR sensor or receive point cloud data.
    '''

    def __init__(self, cfg: dict):
        self.cfg = cfg
        
        # Extract sensor information from the configuration dictionary
        self.manufacturer = self.cfg['sensors']['lidar']['manufacturer'].lower()
        self.model = self.cfg['sensors']['lidar']['model'].lower().replace('-', '')
        self.serial_no = self.cfg['sensors']['lidar']['serial_number']
        self.hostname = self.cfg['sensors']['lidar']['hostname']
        
        # Connect to the LiDAR sensor and initialize the reader
        self.reader = self.__get_reader__()  # the reader should be a generator that yields point cloud data in NumPy array format of shape (N, 4)

    def __get_reader__(self):
        # Generator function that yields point cloud data in NumPy array format of shape (N, 4)
        pass

    def close(self):
        # Release the resources associated with the LiDAR sensor
        self.reader.close()
```

"""