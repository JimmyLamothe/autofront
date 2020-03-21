import contextlib, datetime

def redirect_print(func, *args):
    def wrapper(*args):
        with open('display.txt', 'a') as out:
            with contextlib.redirect_stdout(out):
                print(datetime.datetime.now())
                print(func.__name__)
                return func(*args)
    return wrapper



#Using tempfile - Doesn't work
"""
def redirect_print_temp(func, *args):
    def wrapper(*args):
        with contextlib.redirect_stdout(resources.display):
                print(datetime.datetime.now())
                print(func.__name__)
                return func(*args)
    return wrapper
"""
