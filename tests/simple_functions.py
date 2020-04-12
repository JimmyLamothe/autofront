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
