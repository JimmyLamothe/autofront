""" Utility functions to create routes

This module contains various functions that help create routes
and process user input, especially for live arguments. It calls
on the parse module to parse arguments with type indications.

Key functions:

redirect_print is a decorator that redirects all print calls
to a text file for display in the browser. The original function
does not need to be modified, unless it uses multiprocessing
(if so, see info in docstring).

run_script is used to generate a function that will run the
original script when called from a Flask route.

raise_exceptions is used to activate the exception manager.
When active, runtime exceptions will be displayed in the browser
and the function page will reload. You can create a route to
raise_exceptions to change this functionality live from
the function page.

Other functions are mostly used to process user input.

"""

import contextlib
import pathlib
import subprocess
import functools
from autofront.parse import parse_args, parse_type_args

print_exceptions = True

def browser_exceptions():
    """ Activates display of runtime exceptions in the brower """
    global print_exceptions
    print_exceptions = not print_exceptions



DISPLAY_PATH = str(pathlib.Path(__file__).parent) #Path to display text file

def clear_display():
    """ Clear display text file """
    with open(DISPLAY_PATH + '/display.txt', 'w'):
        pass

def get_display():
    """ Get info from display text file """
    with open(DISPLAY_PATH + '/display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return display

def print_exception(e):
    """ Used by exception manager to print to browser """
    clear_display()
    with open(DISPLAY_PATH + '/display.txt', 'w') as out:
        with contextlib.redirect_stdout(out):
            print(e.__class__.__name__)
            print(e.args[0])

def exception_manager(func):
    """ Decorator to display exceptions in the browser

    Used as a decorator to display runtime exception information
    in the browser instead of raising an exception.

    If you create a route to raise_exceptions, you can switch
    this functionality on or off for all your routes when you want.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if print_exceptions:
            try:
                wrapped_func = func(*args, **kwargs)
            except Exception as e:
                wrapped_func = None
                print_exception(e)
        else:
            wrapped_func = func(*args, **kwargs)
        return wrapped_func
    return wrapper


def redirect_print(func):
    """ Decorator to divert print calls to the browser

    Used as a decorator to print to a file for display
    in the browser instead of to the console.

    If using multiprocessing, it's essential to add "sys.stdout.flush()"
    after the print calls in your child process, otherwise the file
    will only be written on program exit.

    Otherwise, the original function should not need any modification.
    """
    @functools.wraps(func)
    @exception_manager
    def wrapper(*args, **kwargs):
        with open(DISPLAY_PATH + '/display.txt', 'a') as out:
            print('Display path: ' + DISPLAY_PATH)
            with contextlib.redirect_stdout(out):
                #print(datetime.datetime.now()) #Uncomment for debugging
                #print(func.__name__) #Uncomment for debugging
                wrapped_func = func(*args, **kwargs)
                return wrapped_func
    return wrapper

@redirect_print
def print_to_display(string):
    """ Prints any string to the display text_file | str --> None """
    print(string)

def print_return_value(return_value):
    """ Prints the return value of a function | any --> None """
    return_string = str(return_value)
    intro = 'Return value: '
    print_to_display(intro + return_string)

def run_script(script, *args):
    """ Create function to run script for route creation """
    print('running ' + script)
    script_path = './' + script
    command_list = list(args)
    command_list.insert(0, script_path)
    command_list.insert(0, 'python')
    print(command_list)
    def new_function():
        with open(DISPLAY_PATH + '/display.txt', 'a') as out:
            subprocess.run(command_list, stdout=out, check=True)
    new_function.__name__ = script
    return new_function


def add_args_to_title(func_name, arg_list, script=False):
    """ Add fixed args to function name for display in browser """
    title = func_name + ' '
    if not script:
        title += '('
    if arg_list:
        title += ' '
        title += ', '.join(arg_list)
        title += ','
    return title

def get_func_dict(func_title, func_dicts):
    """ Get specific function dict from func_dicts """
    func_dict = [func_dict for func_dict in func_dicts
                 if func_dict['title'] == func_title]
    if len(func_dict) > 1:
        raise Exception('Cannot use same title for your functions')
    func_dict = func_dict[0]
    return func_dict

def get_fixed_args(func_name, func_dicts):
    """ Get fixed args for a function from func_dicts """
    func_dict = get_func_dict(func_name, func_dicts)
    all_fixed_args = []
    fixed_args = func_dict['args']
    fixed_kwargs = func_dict['kwargs']
    all_fixed_args = [fixed_args, fixed_kwargs]
    return all_fixed_args

def get_function(func_title, func_dicts):
    """ Get function from func_dicts """
    func_dict = get_func_dict(func_title, func_dicts)
    function = func_dict['func']
    return function

def live_script(func_title, func_dicts):
    """ Check if script needs live arguments """
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['script'] and func_dict['live']
    return bool_value

def typed_args(func_title, func_dicts):
    """ Check if function uses type indications for its lives args """
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['typed']
    return bool_value

def get_args(request, typed=False):
    """ Get live args input by user """
    arg_string = list(request.form.values())[0]
    if typed:
        all_args = parse_type_args(arg_string)
    else:
        all_args = parse_args(arg_string)
    print('live all args: ' + str(all_args))
    args = all_args[0]
    print('live args: ' + str(args))
    kwargs = all_args[1]
    print('live kwargs: ' + str(kwargs))
    all_args = [args, kwargs]
    print('combined_args: ' + str(all_args))
    return all_args
