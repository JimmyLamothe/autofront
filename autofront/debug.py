""" Decorator to print function steps to console for debugging.

Activate debug_mode to print to console.

Activate step_mode to pause execution at every function return call

Presently only enabled for parsing module.
"""

import functools

debug = False

step = False

def debug_mode():
    """ Activates debug mode """
    global debug
    debug = not debug

def step_mode():
    """ Activates step mode """
    global step
    step = not step

def debug_manager(func):
    """ Decorator. Allows easy debugging """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if debug:
            print('Entering: ' + func.__name__)
            print('Args: ' + str(args))
            print('Kwargs: ' + str(kwargs))
            wrapped_func = func(*args, **kwargs)
            print('Exiting: ' + func.__name__)
            print('Return: ' + str(wrapped_func))
            print('Return type: ' + str(type(wrapped_func)))
            if step:
                input('Press RETURN to continue')
            return wrapped_func
        return func(*args, **kwargs)
    return wrapper
