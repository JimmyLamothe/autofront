import contextlib, datetime

def redirect_print(func, *args):
    def wrapper(*args):
        with open('test.txt', 'a') as out:
            with contextlib.redirect_stdout(out):
                print(datetime.datetime.now())
                print(func.__name__)
                return func(*args)
    return wrapper
