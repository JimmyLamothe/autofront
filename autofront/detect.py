""" Detection of function and script types

Various functions to automatically detect different function and script types
when creating a new route. Automatic detection can be overriden manually
if necessary.

Presently, it's possible to detect whether a route is for a script or a function.

"""

import re

def key_in_kwargs(key, **kwargs):
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
    if type(script_or_function) == str:
        return True
    elif callable(script_or_function):
        return False
    else:
        raise TypeError(script_fail_error)

def detect_input(filepath):
    """ Checks if script has  input calls | script_filepath --> bool """
    input_call = False
    pattern = re.compile(r'\binput\(')
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if pattern.search(line):
            input_call = True
    return input_call
