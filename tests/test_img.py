import os

def test_handler_validity():
    # get all the handlers
    for possible_handler in os.listdir('img'):
        if possible_handler.startswith('handler_') and possible_handler.endswith('.py'):
            # import the handler
            handler = __import__('img.' + possible_handler[:-3], fromlist=['Handler']).Handler
            # handler must be a class not a function
            assert isinstance(handler, type), f"{handler} is not a class"
            # handler must have a close method
            assert hasattr(handler, 'close'), f"{handler} does not have a close method"
            