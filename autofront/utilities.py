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
import atexit
from autofront.parse import parse_args, parse_type_args

print_exceptions = True

def browser_exceptions():
    """ Activates display of runtime exceptions in the brower | None --> None"""
    global print_exceptions
    print_exceptions = not print_exceptions

LOCAL_PATH = pathlib.Path(__file__).parent.joinpath('local') #Path to local files

@atexit.register
def clear_local_path():
    """ Deletes all files in local directory at program exit | None --> None """
    for file in LOCAL_PATH.iterdir():
        print('Deleting: ' + str(file))
        file.unlink()

def insert_lines(readlines_list, index_newline_list):
    """ Inserts lines in file.readlines() list. | [str], [(int, [str])] --> [str]
    
    Takes file.readlines() output list and a list of tuples of line index
    and corresponding list of lines to insert. 
    """
    for tuple in index_newline_list:
        index = tuple[0]
        lines = tuple[1]
        for line in lines:
            readlines_list.insert(index, line)
            index += 1
    return readlines_list

def get_local_filepath(filepath):
    """ Returns local filepath, used to copy a file | str -->  Path"""
    source_path = pathlib.Path(filepath)
    source_name = source_path.name
    new_path = LOCAL_PATH.joinpath(source_name) 
    return new_path

def create_local_script(filepath):
    """ Creates local copy of a script, returns the new filepath | Path --> Path
    
    Changes cwd to original script path to ensure it runs properly
    Adds original script path to sys.path to ensure proper imports
    """
    new_path = get_local_filepath(filepath)
    source_path = pathlib.Path(filepath)
    source_directory = source_path.parent
    SCRIPT_INSERT = ['import os',
                   '\n',
                   'import sys',
                   '\n',
                   'os.chdir("' + str(source_directory.resolve()) + '")',
                   '\n',
                   'sys.path.insert(0, "' + str(source_directory.resolve()) + '")',
                   '\n'
                   ]
    with open(source_path, 'r') as source_script:
        contents = source_script.readlines()
    with open(new_path, 'w') as new_script:
        new_content = insert_lines(contents, [(0, SCRIPT_INSERT)])
        print(new_content)
        new_script.writelines(new_content)
    return new_path

def clear_display():
    """ Clear display text file | None --> None"""
    with open(LOCAL_PATH.joinpath('display.txt'), 'w'):
        pass

def get_display():
    """ Get info from display text file | None --> str"""
    with open(LOCAL_PATH.joinpath('display.txt'), 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return display

def print_exception(e):
    """ Used by exception manager to print to browser | None --> None"""
    clear_display()
    with open(LOCAL_PATH.joinpath('display.txt'), 'w') as out:
        with contextlib.redirect_stdout(out):
            print(e.__class__.__name__)
            print(e.args[0])

def exception_manager(func):
    """ Decorator to display exceptions in the browser | func --> func

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
    """ Decorator to divert print calls to the browser | func --> func

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
        with open(LOCAL_PATH.joinpath('display.txt'), 'a') as out:
            print('Display path: ' + str(LOCAL_PATH.resolve()))
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

def run_script(script_path, *args):
    """ Create function to run script for route creation | str, [str] --> func"""
    print('running ' + script_path.name)
    command_list = list(args)
    command_list.insert(0, script_path.resolve())
    command_list.insert(0, 'python3')
    print(command_list)
    def new_function():
        with open(LOCAL_PATH.joinpath('display.txt'), 'a') as out:
            subprocess.run(command_list, stdout=out, check=True)
    new_function.__name__ = script_path.name
    return new_function


def add_args_to_title(func_name, arg_list, script=False):
    """ Add fixed args to function name for display in browser | str, [str] --> str"""
    title = func_name
    if not script:
        title += ' ('
    if arg_list:
        title += ' '
        title += ', '.join(arg_list)
        title += ','
    return title

def get_func_dict(func_title, func_dicts):
    """ Get specific function dict from func_dicts | str, dict --> dict """
    func_dict = [func_dict for func_dict in func_dicts
                 if func_dict['title'] == func_title]
    if len(func_dict) > 1:
        raise Exception('Cannot use same title for your functions')
    func_dict = func_dict[0]
    return func_dict

def get_fixed_args(func_name, func_dicts):
    """ Get fixed args for a function from func_dicts | str, dict --> [[str],[str]]"""
    func_dict = get_func_dict(func_name, func_dicts)
    all_fixed_args = []
    fixed_args = func_dict['args']
    fixed_kwargs = func_dict['kwargs']
    all_fixed_args = [fixed_args, fixed_kwargs]
    return all_fixed_args

def get_function(func_title, func_dicts):
    """ Get function from func_dicts | str, dict --> func"""
    func_dict = get_func_dict(func_title, func_dicts)
    function = func_dict['func']
    return function

def live_script(func_title, func_dicts):
    """ Check if script needs live arguments | str, dict --> bool"""
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['script'] and func_dict['live']
    return bool_value

def typed_args(func_title, func_dicts):
    """ Check if function uses type indications | str, dict --> bool"""
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['typed']
    return bool_value

def get_args(request, typed=False):
    """ Get live args input by user | request --> [[str], [str]]"""
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
