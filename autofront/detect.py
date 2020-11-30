""" Detection of function and script types

Various functions to automatically detect different function and script types
when adding a new route. Automatic detection can be overriden manually
if necessary.

Presently, it's possible to detect whether a route is for a script or a function.
Future version might detect if a route needs live arguments, for example.

"""

import inspect
import re

def key_in_kwargs(key, **kwargs):
    """ Tests if a key is found in function kwargs | str, kwargs --> bool """
    kwarg_dict = {**kwargs}
    if key in kwarg_dict:
        return True
    return False

def detect_script(script_or_function):
    """ Detects if argument is script or function | obj --> bool

    Returns True for script or False for function
    """
    script_fail_error = 'Failed to detect if route points to script or function.\n'
    script_fail_error += 'Please specify it manually with the script kwarg'
    script_fail_error += ' in autofront.add:\n'
    script_fail_error += 'script=True or script=False'
    if isinstance(script_or_function, str):
        return True
    if callable(script_or_function):
        return False
    raise TypeError(script_fail_error)

#NOTE: The detect input pipeline has been disabled because it was not precise enough.
def detect_input(script_or_function, script=False):
    """ Checks if script or function has input calls | script_or_function --> bool

    NOTE: Not used at present, too many false negatives
    """
    if script:
        script_path = script_or_function
        return detect_input_script(script_path)
    function = script_or_function
    return detect_input_function(function)

def detect_input_script(filepath):
    """ Checks if script has input calls | script_filepath --> bool

    NOTE: Not used at present, too many false negatives
    """
    input_call = False
    pattern = re.compile(r'\binput\(')
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if pattern.search(line):
            input_call = True
    return input_call

def detect_input_function(function):
    """ Checks if function has input calls | function --> bool

    NOTE: Not used at present, too many false negatives
    """
    input_call = False
    source_code = inspect.getsource(function)
    pattern = re.compile(r'\binput\(')
    if pattern.search(source_code):
        input_call = True
    return input_call
