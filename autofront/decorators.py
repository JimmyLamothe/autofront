import contextlib, datetime, sys

"""
Use as a decorator to print to a file for display on screen instead of to the console.
If using multiprocessing, it's essential to add "sys.stdout.flush()" after the print calls
in your child process, otherwise the file will only be written on program exit. Otherwise,
your original function should not need any modification.
"""

def redirect_print(func, *args):
    def wrapper(*args):
        with open('display.txt', 'a') as out:
            with contextlib.redirect_stdout(out):
                #print(datetime.datetime.now()) #Uncomment for debugging
                #print(func.__name__) #Uncomment for debugging
                wrapped_func = func(*args)
                return wrapped_func
    return wrapper
