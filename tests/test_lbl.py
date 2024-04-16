import os

def test_handler_validity():
    # get all the handlers
    for possible_handler in os.listdir('lbl'):
        if possible_handler.startswith('handler_') and possible_handler.endswith('.py'):
            # import the handler
            handler = __import__('lbl.' + possible_handler[:-3], fromlist=['*'])
            # handler must have a colors attribute
            assert hasattr(handler, 'colors'), f"{handler} does not have a colors attribute"
            # handler must have a label_file_extension attribute
            assert hasattr(handler, 'label_file_extension'), f"{handler} does not have a label_file_extension attribute"
            # label_file_extension must be a string
            assert isinstance(handler.label_file_extension, str), f"{handler.label_file_extension} is not a string"
            # label_file_extension must start with a period
            assert handler.label_file_extension[0] == '.', f"{handler.label_file_extension} is not a valid file extension"
            # check if the handler is callable
            assert callable(handler.Handler), f"{handler.Handler} is not callable"