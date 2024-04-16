import os

def test_handler_validity():
    # get all the handlers
    for possible_handler in os.listdir('calib'):
        if possible_handler.startswith('handler_') and possible_handler.endswith('.py'):
            # import the handler
            handler = __import__('calib.' + possible_handler[:-3], fromlist=['*'])
            handler_calib_file_extension = handler.calib_file_extension
            handler = handler.Handler
            # check if the handler has a calib_file_extension attribute
            assert handler_calib_file_extension[0] == '.', f"calib_file_extension is not a valid file extension"
            # check if the handler is callable
            assert callable(handler), f"{handler} is not callable"