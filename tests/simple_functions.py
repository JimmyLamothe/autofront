""" Test functions for autofront test suite

All these functions are imported by autotest.py and used to test
the package.
"""

def bugged_function():
    """ Test function to test exception management | str --> Exception """
    test_list = [0, 1]
    print(test_list[2]) #should raise exception

def foo():
    """ Test function for simple functions | str --> None """
    print('bar')

def bar():
    """ Test function for simple functions | str --> None """
    print('foo')

def foo_args(arg1, arg2, kwarg1 = 'kwarg1', kwarg2 = 'kwarg2'):
    print(arg1, arg2, kwarg1, kwarg2)

def return_value():
    """ Test function for return values | str --> str """
    return 'foo'

def positional(arg1, arg2):
    """ Test function for live args | str --> None """
    print('Positional ' + arg2 + ' ' + arg1)

def keywords(kwarg1=None, kwarg2=None):
    """ Test function for live kwargs | str --> None """
    print('Keywords: ' + kwarg2 + ' ' + kwarg1)

def combined(arg1, arg2, kwarg1=None, kwarg2=None):
    """ Test function for live args and kwargs | str --> None"""
    print('Combined: ' + kwarg2 + ' ' + kwarg1 + ' ' + arg2 + ' ' + arg1)

def mixed_args(fixed1, fixed2, var1, var2, kwarg1=None, kwarg2=None):
    """ Test function for mix of fixed and live args | str --> None """
    print('Builtin: ' + kwarg2 + ' ' + kwarg1 + ' ' + var2 + ' ' + var1 + ' ' +
          fixed2 + ' ' + fixed1)

def return_value_args(arg1, arg2, kwarg1=None, kwarg2=None):
    """ Test function for return values with live args | str --> None """
    return [arg1, arg2, kwarg1, kwarg2]

def types(*args):
    """ Test function for live typed args | str--> None """
    print('Here are your args and their type:')
    for arg in args:
        print(arg, str(type(arg)))
        print('In string form: ' + str(arg))
    
def types_kwarg(*args, **kwargs):
    """ Test function for live typed args and kwargs | str --> None

    Input following arguments in browser to test:
    
    str:foo, int:3, tuple:(str:bar, list:[str:foobar]),
    list:[dict:{str:foo : str:bar}, tuple:(bool:True, bool:False)],
    dict:{str:bar : int:2, str:barfoo : list:[int:2, int:3, int:4]}
    """

    print('Here are your args and their type:')
    for arg in args:
        print(arg, str(type(arg)))
    print('Here are your kwargs and their type:')
    for key, value in kwargs.items():
        print('Key: ' + str(key) + ' ' + str(type(key)))
        print('Value: ' + str(value) + ' ' + str(type(value)))

def return_value_types_args(*args, **kwargs):
    """ Test function for return values with live typed args """
    return [args, kwargs]
