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
import re
import subprocess
import functools
import time
from autofront.parse import parse_args, parse_type_args

print_exceptions = True

input_received = False

def browser_exceptions():
    """ Activates display of runtime exceptions in the brower | None --> None"""
    global print_exceptions
    print_exceptions = not print_exceptions
    if print_exceptions:
        print('Activated browser exceptions')
    else:
        print('Deactivated browser exceptions')

LOCAL_PATH = pathlib.Path(__file__).parent.joinpath('local') #Path to local files

def clear_local_files():
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

def web_input(prompt):
    """ Replaces the built-in input function for browser input | str --> str 
    
    Writes input prompt to prompt file to activate browser_input.
    Browser input gets user input in browser and writes to input file.
    Reads input file and returns it just as for original input call.
    """
    clear_input()
    input_received = False
    with open(LOCAL_PATH.joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write(prompt)
    while not input_received:
        with open(LOCAL_PATH.joinpath('input.txt'), 'r') as input_file:
            if not input_file.read():
                time.sleep(1)
            else:
                input_received=True
                return input_file.read()

def get_prompt():
    """ Waits for prompt file to be written and returns contents | None --> str """
    clear_prompt()
    prompt_received = False
    while not prompt_received:
        with open(LOCAL_PATH.joinpath('prompt.txt'), 'r') as prompt_file:
            if not prompt_file.read():
                time.sleep(1)
            else:
                prompt_received=True
                return prompt_file.read()

def count_input(filepath):
    input_count = 0
    pattern = re.compile(r'\binput\(')
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if pattern.search(line):
            input_count += 1
    return input_count

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
                     'from autofront.utilities import web_input',
                     '\n',
                     'input = web_input',
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
    """ Clear display text file | None --> None """
    with open(LOCAL_PATH.joinpath('display.txt'), 'w'):
        pass

def clear_prompt():
    """ Clear prompt text file | None --> None """
    with open(LOCAL_PATH.joinpath('prompt.txt'), 'w'):
        pass

def clear_input():
    """ Clear input text file | None --> None """
    with open(LOCAL_PATH.joinpath('input.txt'), 'w'):
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

def is_script(func_title, func_dicts):
    """ Check if script | str, dict --> bool"""
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['script']
    return bool_value

def is_live(func_title, func_dicts):
    """ Check if script or function needs live arguments | str, dict --> bool"""
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['live']
    return bool_value

def input_script(func_title, func_dicts):
    """ Check how many times script needs user input | str, dict --> bool or int
    
    Returns False if no input required.

    Returns Int with number of input calls otherwise
    """
    func_dict = get_func_dict(func_title, func_dicts)
    input_value = func_dict['input']
    return input_value

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
