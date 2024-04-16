import os

img_dir = os.path.dirname(os.path.realpath(__file__))

supported_manufacturers = [sm.split('_')[1] for sm in os.listdir(img_dir) if 'handler' in sm]
supported_models = [sm.split('_')[2].replace('.py','') for sm in os.listdir(img_dir) if 'handler' in sm]

class SensorIO:
    """
    A class representing the sensor input/output for image processing.

    Args:
        cfg (dict): The configuration dictionary containing sensor information.

    Attributes:
        manufacturer (str): The manufacturer of the camera sensor.
        model (str): The model of the camera sensor.
        serial_no (str): The serial number of the camera sensor.
        cfg (dict): The configuration dictionary.
        img_count (int): The number of images in the data.
        handle (Handler): The handler for reading the sensor data.
        reader (Iterator): The iterator for reading the sensor data.
        idx (int): The current index of the sensor data.

    Methods:
        __getitem__(self, idx): Retrieves the image at the specified index.
        __len__(self): Returns the number of images in the data.
        close(self): Closes the sensor data handler.

    Raises:
        NotImplementedError: If the manufacturer or model is not supported.

    """

    def __init__(self, cfg: dict):
        self.manufacturer = cfg['sensors']['camera']['manufacturer'].lower()
        self.model = cfg['sensors']['camera']['model'].lower().replace('-','')
        self.serial_no = cfg['sensors']['camera']['serial_number']
        
        # Check if the manufacturer and model are supported
        if self.manufacturer not in supported_manufacturers: raise NotImplementedError("Manufacturer not supported. Supported manufacturers: " + ', '.join(supported_manufacturers) + ".")
        if self.model not in supported_models: raise NotImplementedError("Model not supported. Supported models: " + ', '.join(supported_models) + ".")
        
        self.cfg = cfg
        self.img_count = cfg['data']['size']
        # Import the handler for the sensor data
        handler = __import__('img.handler_'+self.manufacturer+'_'+self.model, fromlist=['Handler']).Handler
        self.handle = handler(self.cfg)
        self.reader = self.handle.reader
        self.idx = -1
        
    def __getitem__(self, idx):
        """
        Retrieves the image at the specified index.

        Args:
            idx (int): The index of the image to retrieve.

        Returns:
            tuple: A tuple containing None and the RGB image.

        """
        if idx > self.idx:
            img_bgr = next(self.reader)
            self.img_rgb = img_bgr[:,:,::-1].copy()
            self.idx = idx
        return None, self.img_rgb # return None as the label_path because it is from live sensor data
        
    def __len__(self):
        """
        Returns the number of images in the data.

        Returns:
            int: The number of images in the data.

        """
        return self.img_count
    
    def close(self):
        """
        Closes the sensor data handler.

        """
        self.handle.close()
    
    