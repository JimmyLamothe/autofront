""" Detection of function and script types

Various functions to automatically detect different function and script types
when creating a new route. Automatic detection can be overriden manually
if necessary.

Presently, it's possible to detect whether a route is for a script or a function,
as well as if a script or function might require input calls.

Detection for input calls is very simple and only checks if an input call takes place
in the script or function specified in create_route. Any input calls in modules imported
by the script or present in other functions used by the function are not checked for.
An input call might be detected that only rarely or ever is actually called.
In this case, it might be better to specify detect=False or a very low timeout value
when creating the route.

"""

import inspect
import re

def key_in_kwargs(key, **kwargs):
    """ Tests if a key is found in function **kwargs | str, kwargs --> bool """
    kwarg_dict = {**kwargs}
    if key in kwarg_dict:
        return True
    return False

def detect_script(script_or_function):
    """ Detects if argument is script or function | obj --> bool """
    script_fail_error = 'Failed to detect if route points to script or function.\n'
    script_fail_error += 'Please specify it manually with the script kwarg'
    script_fail_error += ' in create_route:\n'
    script_fail_error += 'script=True or script=False'
    if isinstance(script_or_function, str):
        return True
    if callable(script_or_function):
        return False
    raise TypeError(script_fail_error)

def detect_input(script_or_function, script=False):
    """ Checks if script has  input calls | script_filepath --> bool """
    if script:
        script_path = script_or_function
        return detect_input_script(script_path)
    function = script_or_function
    return detect_input_function(function)

def detect_input_script(filepath):
    """ Checks if script has input calls | script_filepath --> bool """
    input_call = False
    pattern = re.compile(r'\binput\(')
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if pattern.search(line):
            input_call = True
    return input_call

def detect_input_function(function):
    """ Checks if function has input calls | script_filepath --> bool """
    input_call = False
    source_code = inspect.getsource(function)
    pattern = re.compile(r'\binput\(')
    if pattern.search(source_code):
        input_call = True
    return input_call
