import os

pcd_dir = os.path.dirname(os.path.realpath(__file__))

supported_manufacturers = [sm.split('_')[1] for sm in os.listdir(pcd_dir) if 'handler' in sm]
supported_models = [sm.split('_')[2].replace('.py','') for sm in os.listdir(pcd_dir) if 'handler' in sm]

class SensorIO:
    def __init__(self, cfg: dict):
        """
        Initializes the SensorIO class.

        Args:
            cfg (dict): Configuration dictionary containing sensor information.

        Raises:
            NotImplementedError: If the manufacturer or model is not supported.
        """
        self.manufacturer = cfg['sensors']['lidar']['manufacturer'].lower()
        self.model = cfg['sensors']['lidar']['model'].lower().replace('-', '')
        self.serial_no = cfg['sensors']['lidar']['serial_number']
        
        # Check if the manufacturer is supported
        if self.manufacturer not in supported_manufacturers:
            raise NotImplementedError("Manufacturer not supported. Supported manufacturers: " + ', '.join(supported_manufacturers) + ".")
        
        # Check if the model is supported
        if self.model not in supported_models:
            raise NotImplementedError("Model not supported. Supported models: " + ', '.join(supported_models) + ".")
        
        self.cfg = cfg
        self.pcd_count = cfg['data']['size']
        
        # Import the appropriate handler based on the manufacturer and model
        handler = __import__('pcd.handler_'+self.manufacturer+'_'+self.model, fromlist=['Handler']).Handler
        
        self.handle = handler(self.cfg)
        self.reader = self.handle.reader
        self.idx = -1
        
    def __getitem__(self, idx):
        """
        Returns the item at the given index.

        Args:
            idx (int): Index of the item.

        Returns:
            tuple: A tuple containing None and the pcd_intensity_np array.
        """
        if idx > self.idx:
            self.pcd_intensity_np = next(self.reader)
            self.idx = idx
        return None, self.pcd_intensity_np
        
    def __len__(self):
        """
        Returns the number of items in the SensorIO object.

        Returns:
            int: Number of items.
        """
        return self.pcd_count
    
    def close(self):
        """
        Closes the SensorIO object.
        """
        self.handle.close()
