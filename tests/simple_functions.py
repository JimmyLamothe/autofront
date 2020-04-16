def bugged_function():
    test_list = [0, 1]
    print(test_list[2]) #should raise exception

def foo():
    print('bar')

def bar():
    print('foo')

def positional(arg1, arg2):
    print('Positional ' + arg2 + ' ' + arg1)

def keywords(arg1 = None, arg2 = None):
    print('Keywords: ' + arg2 + ' ' + arg1)

def combined(arg1, arg2, arg3 = None, arg4 = None):
    print('Combined: ' + arg4 + ' ' + arg3 + ' ' + arg2 + ' ' + arg1)

def mixed_args(fixed1, fixed2, var3, var4, arg5 = None, arg6 = None):
    print('Builtin: ' + arg6 + ' ' + arg5 + ' ' + var4 + ' ' + var3 + ' ' +
          fixed2 + ' ' + fixed1)

def types(*args):
    print('Here are your args and their type:')
    for arg in args:
        print(arg, str(type(arg)))
        print('In string form: ' + str(arg))
    
def types_kwarg(*args, **kwargs):
    print('Here are your args and their type:')
    for arg in args:
        print(arg, str(type(arg)))
    print('Here are your kwargs and their type:')
    for key, value in kwargs.items():
        print('Key: ' + str(key) + ' ' + str(type(key)))
        print('Value: ' + str(value) + ' ' + str(type(value)))

"""
Use following arguments to test:

str:foo, int:3, tuple:(str:bar, list:[str:foobar]), list:[dict:{str:foo : str:bar}, tuple:(bool:True, bool:False)], dict:{str:bar : int:2, str:barfoo : list:[int:2, int:3, int:4]}
"""
