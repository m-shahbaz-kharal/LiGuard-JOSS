class Handler:
    """
    A class that handles the FLIR camera operations.

    Args:
        cfg (dict): Configuration dictionary containing camera settings.

    Attributes:
        manufacturer (str): The manufacturer of the camera.
        model (str): The model of the camera.
        serial_no (str): The serial number of the camera.
        system (pyspin.System): The PySpin system instance.
        camera (pyspin.Camera): The PySpin camera instance.
        reader (generator): A generator that yields image arrays.

    Raises:
        Exception: If no FLIR camera is connected to the system.

    """

    def __init__(self, cfg):
        try: pyspin = __import__('PySpin')
        except:
            print("Spinnaker SDK not installed.\nPlease download resource at from https://flir.netx.net/file/asset/59493/original/attachment and please install the wheel using `pip install spinnaker_python-4.0.0.116-cp310-cp310-win_amd64.whl.")
            return

        self.manufacturer = cfg['sensors']['camera']['manufacturer'].lower()
        self.model = cfg['sensors']['camera']['model'].lower().replace('-', '')
        self.serial_no = cfg['sensors']['camera']['serial_number'].lower()

        self.system = pyspin.System.GetInstance()
        camera_list = self.system.GetCameras()

        # Check if there is a FLIR camera connected to the system
        if camera_list.GetSize() == 0:
            self.system.ReleaseInstance()
            raise Exception("There is no FLIR camera connected to the system.")

        self.camera = camera_list.GetBySerial(self.serial_no)
        self.camera.Init()

        # start the camera
        self.camera.BeginAcquisition()

        self.reader = self.__get__reader__()

    def __get__reader__(self):
        """
        A generator that continuously yields image arrays from the camera.

        Yields:
            numpy.ndarray: The next image array from the camera.

        """
        while True:
            image_result = self.camera.GetNextImage(10)  # 10 ms timeout
            if image_result.IsIncomplete():
                print('An incomplete image is received. Dropping ...')
            else:
                img_np = image_result.GetNDArray()
                image_result.Release()
                yield img_np

    def close(self):
        """
        Closes the camera and releases resources.

        """
        self.reader.close()
        self.camera.EndAcquisition()
        self.camera.DeInit()
        del self.camera
        self.system.ReleaseInstance()