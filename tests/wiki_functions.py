""" Functions used by autowiki.py to generate screen shots for the wiki """

def my_function():
    print('This is a print call')
    return('This is a return value')

def my_live_function(arg1, arg2, kwarg1=None, kwarg2=None):
    print('Here are my args:')
    return([arg1, arg2, kwarg1, kwarg2])

def my_mixed_function(arg1, arg2, kwarg1=None, kwarg2=None):
    print('Here are my args')
    return [arg1, arg2, kwarg1, kwarg2]

def my_typed_function(*args, **kwargs):
    print('Here are my args and their type:')
    for arg in args:
        print(arg, str(type(arg)))
    print('Here are my kwargs and their type:')
    for key, value in kwargs.items():
        print('Key: ' + str(key) + ' ' + str(type(key)))
        print('Value: ' + str(value) + ' ' + str(type(value)))
