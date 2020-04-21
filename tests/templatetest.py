""" Test module for autofront package

This module tests the custom template functionality.

"""
import sys

args = sys.argv

if len(args) > 1:
    if args[1] == 'dev': #This is only used for development. 
        sys.path.insert(1, '/Users/jimmy/Programming/Python/autofront/')
        import autofront
    else:
        sys.exit('invalid argument')
else:
    import autofront

from simple_functions import foo, bar, positional, keywords, combined
from simple_functions import mixed_args, bugged_function, types, types_kwarg
from simple_functions import foo_args, return_value, return_value_args
from simple_functions import return_value_types_args

template_path = '/Users/jimmy/Programming/Python/autofront/tests/templates'

autofront.initialize(raise_exceptions=True, template_folder=template_path)

autofront.create_route(bugged_function)

autofront.create_route(foo)

autofront.create_route(bar)

autofront.create_route(foo_args, 'arg1', 'arg2',
                       kwarg1='Surprise!', kwarg2='Aha!')

autofront.create_route(return_value)

autofront.create_route('simple_script.py', script=True)

autofront.create_route('simple_script_args.py', 'foo', 'bar', 'foobar',
                       script=True)

autofront.create_route('simple_script_args.py', link='forgotargs',
                       title='simple_script_args.py without args',
                       script=True)

autofront.create_route(positional, live=True)

autofront.create_route(keywords, live=True)

autofront.create_route(combined, live=True)

autofront.create_route(mixed_args, 'fixed1', 'fixed2', live=True)

autofront.create_route(return_value_args, live=True)

autofront.create_route('simple_script_live.py', script=True, live=True)

autofront.create_route(types, live=True, typed=True)

autofront.create_route(types_kwarg, live=True, typed=True)

autofront.create_route(return_value_types_args, live=True, typed=True)

autofront.create_route(autofront.utilities.browser_exceptions)

autofront.create_route(autofront.debug.debug_mode)

autofront.create_route(autofront.debug.step_mode)

autofront.run()
