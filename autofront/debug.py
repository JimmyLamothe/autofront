import functools

"""
Used as a decorator to print function steps to console for debugging.
"""

debug = True

step = False

def debug_mode():
    global debug
    debug = not debug

def step_mode():
    global step
    step = not step

def debug_manager(func):
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
