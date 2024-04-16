# contains algorithms that are used to manipulate/transform the calibration parameters

from gui.logger_gui import Logger

def dummy(data_dict: dict, cfg_dict: dict):
    # get logger object from data_dict
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->calib.py->dummy][CRITICAL]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return

    # do stuff
    # ...

    # logging operation
    logger.log('[algo->pre.py->dummy]: A dummy function is called.', Logger.DEBUG)