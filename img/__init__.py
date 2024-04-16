"""
The img package comprises two types of handlers: (1) file handlers for reading image files and (2) sensor handlers for capturing images from live camera feeds. The `file_io.py` and `sensor_io.py` modules should not be modified except for contributions to the framework application logic.

### Creating a New Sensor Stream Handler:

To create a new sensor stream handler to support a new camera sensor:

1. Create a new Python file named `handler_<manufacturer>_<model>.py` in the `img` directory.
2. Replace `<manufacturer>` and `<model>` with the respective manufacturer and model of the camera.
3. The manufacturer and model are passed from `config.yml` under `sensors:camera:manufacturer` and `sensors:camera:model`, respectively, and are used to select the appropriate handler.

### Handler File Structure:

The `handler_<manufacturer>_<model>.py` file should contain a class named `Handler` with the following structure:

```python
# hander_<manufacturer>_<model>.py

class Handler:
    '''
    Args:
        cfg (dict): Configuration dictionary containing camera settings.

    Attributes:
        manufacturer (str): The manufacturer of the camera.
        model (str): The model of the camera.
        serial_no (str): The serial number of the camera.
        reader (generator): A generator that yields image arrays.

    Raises:
        Exception: If fails to connect to the camera or receive images from it.
    '''

    def __init__(self, cfg):
        self.manufacturer = cfg['sensors']['camera']['manufacturer'].lower()
        self.model = cfg['sensors']['camera']['model'].lower().replace('-', '')
        self.serial_no = cfg['sensors']['camera']['serial_number'].lower()

        # Connect to the camera and initialize the reader
        self.reader = self.__get_reader__()

    def __get_reader__(self):
        # Return a generator that yields image arrays
        pass

    def close(self):
        # Release the camera resources
        self.reader.close()
```

"""