""" Test module for autofront package

This module starts a Flask server with routes to all the different functions
in simple_functions.py, which should test all the basic functionality
provided by the package. After any code change, make sure to run these tests
and to check everything is still kosher.

Consult the autofront wiki at https://github.com/JimmyLamothe/autofront/issues
to check the required input and expected output for each route.

"""
import autofront
from simple_functions import foo, bar, positional, keywords, combined
from simple_functions import mixed_args, bugged_function, types, types_kwarg
from simple_functions import foo_args, return_value, return_value_args
from simple_functions import return_value_types_args, input_function

#Basic routes to functions with no args or kwargs
autofront.create_route(foo)
#Route to function with fixed args and kwargs
autofront.create_route(foo_args, 'arg1', 'arg2',
                       kwarg1='Surprise!', kwarg2='Aha!')
#Route to function which returns a value
autofront.create_route(return_value)
#Basic route to script with no command-line args
autofront.create_route('simple_script.py')
#Route to script with fixed command-line args
autofront.create_route('simple_script_args.py', 'foo', 'bar', 'foobar')
#Route to show title syntax for duplicate functions and scripts
autofront.create_route('simple_script_args.py', link='forgotargs',
                       title='simple_script_args.py without args')
#Route to test import behavior for scripts
autofront.create_route('import_script.py')
#Route to script requiring user input
autofront.create_route('input_script.py')
#Route to script which might or might not ask for input
autofront.create_route('conditional_input_script.py', live=True)
#Route to longer input script in honor of my niece Joëlle
autofront.create_route('test_joelle.py')
#Route to function requiring user input
autofront.create_route(input_function)
#Route to function meant to run in background
autofront.create_route('background_script.py', join=False)
#Route to same background function, but wait until it exits
autofront.create_route('background_script.py', title='timeout test',
                       timeout=2)
#Route to function requiring live args
autofront.create_route(positional, live=True)
#Route to function requiring live kwargs
autofront.create_route(keywords, live=True)
#Route to function requiring live args and live kwargs
autofront.create_route(combined, live=True)
#Route to function requiring both fixed and live args
autofront.create_route(mixed_args, 'fixed1', 'fixed2', live=True)
#Route to function with live args and a return value
autofront.create_route(return_value_args, live=True)
#Route to script with live command line args
autofront.create_route('simple_script_live.py', live=True)
#Route to script with live typed args
autofront.create_route(types, live=True, typed=True)
#Route to script with live typed kwargs
autofront.create_route(types_kwarg, live=True, typed=True)
#Route to script with live typed args and kwargs with a return value
autofront.create_route(return_value_types_args, live=True, typed=True)
#Route to bugged function - Exception should print in browser
autofront.create_route(bugged_function)
#Route to bugged script - Exception should print in browser
autofront.create_route('bugged_script.py')

autofront.run()
