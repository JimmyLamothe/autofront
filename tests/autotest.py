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

from simple_functions import foo, bar, positional, keywords, combined
from simple_functions import mixed_args, bugged_function
from simple_args import foo_args

print('Print exceptions : ' + str(autofront.utilities.print_exceptions))

autofront.create_route(bugged_function)

autofront.create_route(foo)

autofront.create_route(bar)

autofront.create_route(foo_args, 'arg1', 'arg2', arg3 = 'arg5', arg4 = 'arg6')

autofront.create_route('simple_script.py', script = True)

autofront.create_route('simple_script_args.py', 'foo', 'bar', 'foobar',
                       script = True)

autofront.create_route('simple_script_args.py', link = 'forgotargs',
                       title = 'simple_script_args.py without args',
                       script = True)

autofront.create_route(positional, live = True)

autofront.create_route(keywords, live = True)

autofront.create_route(combined, live = True)

autofront.create_route(mixed_args, 'fixed1', 'fixed2', live = True)

autofront.create_route('simple_script_live.py', script = True, live = True)

autofront.create_route(autofront.utilities.raise_exceptions)


autofront.run()

