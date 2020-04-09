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
