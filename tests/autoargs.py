import sys

args = sys.argv

if len(args) > 1:
    if args[1] == 'dev':
        sys.path.insert(1, '/Users/jimmy/Programming/Python/autofront/')
        import autofront
    else:
        sys.exit('invalid argument')
else:
    import autofront

from simple_args import foo

autofront.create_route(foo, 'arg1', 'arg2', arg3 = 'arg5', arg4 = 'arg6')

autofront.run()
