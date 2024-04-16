import numpy as np

class Handler:
    """
    A class that handles the Ouster OS1-64 LiDAR sensor.

    Args:
        cfg (dict): Configuration dictionary containing sensor information.

    Attributes:
        cfg (dict): Configuration dictionary containing sensor information.
        manufacturer (str): Manufacturer of the LiDAR sensor.
        model (str): Model of the LiDAR sensor.
        serial_no (str): Serial number of the LiDAR sensor.
        hostname (str): Hostname of the LiDAR sensor.
        client (ouster.client): Ouster client object.
        stream (ouster.client.Scans): Scans stream object.
        xyz_lut (ouster.client.XYZLut): XYZ lookup table object.
        reader (generator): Generator that yields point cloud data.

    """

    def __init__(self, cfg: dict):
        try: ouster = __import__('ouster', fromlist=['client'])
        except:
            print("Ouster-SDK not installed, please install it using 'pip install ouster-sdk'.")
            return
        self.cfg = cfg
        
        # Extract sensor information from the configuration dictionary
        self.manufacturer = self.cfg['sensors']['lidar']['manufacturer'].lower()
        self.model = self.cfg['sensors']['lidar']['model'].lower().replace('-','')
        self.serial_no = self.cfg['sensors']['lidar']['serial_number']
        self.hostname = self.cfg['sensors']['lidar']['hostname']
        
        self.client = ouster.client
        
        # Set the sensor config
        config = self.client.SensorConfig()
        config.udp_port_lidar = 7502
        config.udp_port_imu = 7503
        config.operating_mode = self.client.OperatingMode.OPERATING_NORMAL
        if self.hostname == 'localhost':
            self.hostname = 'os-' + self.serial_no + '.local'
        self.client.set_config(self.hostname, config, udp_dest_auto=True)
        
        try:
            # Create the scans stream and XYZ lookup table
            self.stream = self.client.Scans.stream(hostname=self.hostname, lidar_port=config.udp_port_lidar)
            self.xyz_lut = self.client.XYZLut(self.stream.metadata)
        except Exception as e:
            raise Exception(f"Error connecting to Ouster OS1-64: {e}")
            
        self.reader = self.__get_reader__()

    def __get_reader__(self):
        """
        Generator function that yields point cloud data.

        Yields:
            np.ndarray: Numpy array containing point cloud data.

        """
        while True:
            for scan in self.stream:
                pcd_xyz = self.xyz_lut(scan).reshape(-1, 3)
                intensity = self.client.destagger(self.stream.metadata, scan.field(self.client.ChanField.REFLECTIVITY)).reshape(-1, 1)
                pcd_intensity_np = np.hstack((pcd_xyz, intensity))
                yield pcd_intensity_np
                
    def close(self):
        """
        Closes the reader and stream objects.

        """
        self.reader.close()
        self.stream.close()