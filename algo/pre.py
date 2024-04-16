from gui.logger_gui import Logger

# another dummy function, please read algo/calib.py for more information on how to create a function
def dummy(data_dict: dict, cfg_dict: dict):
    # get logger object from data_dict
    if 'logger' in data_dict: logger:Logger = data_dict['logger']
    else: print('[algo->pre.py->dummy][CRITICAL]: No logger object in data_dict. It is abnormal behavior as logger object is created by default. Please check if some script is removing the logger key in data_dict.'); return

    # do stuff
    # ...

    # logging
    logger.log('[algo->pre.py->dummy]: A dummy function is called.', Logger.DEBUG)