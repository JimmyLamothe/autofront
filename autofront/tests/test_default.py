""" Test module for autofront package

This module starts a Flask server with routes to all the different functions
in simple_functions.py, which should test all the basic functionality
provided by the package. After any code change, make sure to run these tests
and to check everything is still kosher.

"""
import autofront
from simple_functions import foo, bar, positional, keywords, combined
from simple_functions import mixed_args, bugged_function, types, types_kwarg
from simple_functions import foo_args, return_value, return_value_args
from simple_functions import return_value_types_args, input_function

print('Print exceptions : ' + str(autofront.utilities.print_exceptions))

autofront.create_route(bugged_function)

autofront.create_route(foo)

autofront.create_route(bar)

autofront.create_route(foo_args, 'arg1', 'arg2',
                       kwarg1='Surprise!', kwarg2='Aha!')

autofront.create_route(return_value)

#Remove dev from script args to test pip package
autofront.create_route('simple_script.py')

autofront.create_route('simple_script_args.py', 'foo', 'bar', 'foobar')

autofront.create_route('simple_script_args.py', link='forgotargs',
                       title='simple_script_args.py without args')

autofront.create_route('import_script.py')

autofront.create_route('input_script.py')

autofront.create_route('conditional_input_script.py', live=True)

autofront.create_route('test_joelle.py')

autofront.create_route(input_function)

autofront.create_route(positional, live=True)

autofront.create_route(keywords, live=True)

autofront.create_route(combined, live=True)

autofront.create_route(mixed_args, 'fixed1', 'fixed2', live=True)

autofront.create_route(return_value_args, live=True)

autofront.create_route('simple_script_live.py', live=True)

autofront.create_route(types, live=True, typed=True)

autofront.create_route(types_kwarg, live=True, typed=True)

autofront.create_route(return_value_types_args, live=True, typed=True)

autofront.create_route(autofront.utilities.browser_exceptions)

autofront.create_route(autofront.debug.debug_mode)

autofront.create_route(autofront.debug.step_mode)

autofront.run()

