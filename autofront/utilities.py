""" Utility functions


This module contains various functions that help create routes
and process user input for live arguments. It calls on the parse module
to parse arguments with type indications.

"""

import atexit
import contextlib
import functools
import pathlib
import pprint
import subprocess
from autofront.config import config, status
from autofront.parse import parse_args, parse_type_args

def get_shell_python_version(command='python -V'):
    """ Get version of Python running in shell | None --> tuple
    
    Use command keyword to test python3 instead of python
    if python version is Python 2.

    Minor version is not used at present but is included in case it is needed
    in future versions.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    version_string = result.stdout
    if not version_string: #For some reason Python 2 goes to stderr
        version_string = result.stderr
    print('version_string is: {}'.format(version_string))
    major_version_index = version_string.find(' ') + 1
    major_version = int(version_string[major_version_index])
    minor_version_index = version_string.find('.') + 1
    minor_version = int(version_string[minor_version_index])
    revision_index = version_string.find('.') + 3
    revision = int(version_string[revision_index])
    return tuple([major_version, minor_version, revision])

def get_python_command():
    """ Get version of python command necessary to run scripts with Python 3
    in the shell. 

    It's possible to ignore the result and force autofront to run scripts
    using Python 2 with the 'allow_python_2' keyword argument
    in autofront.initialize.
    """
    print('testing "python" command')
    version = get_shell_python_version()
    major_version = version[0]
    minor_version = version[1]
    revision = version[2]
    if major_version == 2:
        print('testing "python3" command')
        try:
            major_version = get_shell_python_version(command='python3 -V')[0]
            if major_version == 3:
                print('Scripts will be run in shell with "python3" command')
                print('Shell Python version is {0}.{1}.{2}'.format(major_version,
                                                                   minor_version,
                                                                   revision))
                return 'python3'
            else:
                print('Error identifying correct python command to run scripts.')
                print("Defaulting to 'python'")
        except IndexError:
            print('Warning: Your shell environment is in Python 2.')
            print('Scripts will be run using the Python 2 interpreter')
            print('Shell Python version is {0}.{1}.{2}'.format(major_version,
                                                           minor_version,
                                                           revision))
    else:
        print('Scripts will be run in shell with "python" command')
        print('Shell Python version is {0}.{1}.{2}'.format(major_version,
                                                           minor_version,
                                                           revision))
    return 'python'

def set_run_flag():
    """ Set flag on server start | None --> None """
    with open(get_local_path().joinpath('server_running.txt'), 'w') as flag:
        flag.write('True')

def get_run_flag():
    """ Check if server is already running | None --> Bool
    
    This is used to prevent child processes from trying to reinitialize
    or restart the server.
    """
    try:
        with open(get_local_path().joinpath('server_running.txt'), 'r') as flag:
            if flag.read() == 'True':
                return True
            return False
    except FileNotFoundError:
        return False

def check_for_main():
    """ Returns false if not in main process | None --> Bool
    
    This check replaces the standard if __name__ == '__main__' used
    with the multiprocessing module to prevent child processes from
    running functions when they import the main module.
    """
    if get_run_flag():
        return False
    return True

def get_child_flag():
    """ Get number of running child processes | None --> Bool """
    try:
        with open(get_local_path().joinpath('child_processes.txt'), 'r') as flag:
            value = flag.read()
            print('current child processes : {}'.format(str(value)))
            return int(value)
    except FileNotFoundError:
        with open(get_local_path().joinpath('child_processes.txt'), 'w') as flag:
            flag.write('0')
        return 0
    
def increment_child_flag():
    """ Increase count of running child processes | None --> None """
    old = get_child_flag()
    print('old value: {}'.format(str(old)))
    new = old + 1
    print('new value: {}'.format(str(new)))
    with open(get_local_path().joinpath('child_processes.txt'), 'w') as flag:
        flag.write(str(new))

@atexit.register
def decrement_child_flag():
    """ Decrease count of running child processes | None --> None
    
    Automatically runs on process exit to ensure proper count.
    """
    old = get_child_flag()
    print('old value: {}'.format(str(old)))
    new = max(0, old - 1)
    print('new value: {}'.format(str(new)))
    with open(get_local_path().joinpath('child_processes.txt'), 'w') as flag:
        flag.write(str(new))

def get_local_path():
    """ Get local path from config.py | None --> Path

    The local path is where all temporary files are created.
    They are deleted on program exit.

    """
    return config['local_path']

def browser_exceptions():
    """ Activate display of runtime exceptions in the brower | None --> None

    When active, runtime exceptions raised by a route function or script
    are displayed in the browser if possible. Otherwise, they print to the console.

    """
    config['print_exceptions'] = not config['print_exceptions']
    if config['print_exceptions']:
        print('Activated browser exceptions')
    else:
        print('Deactivated browser exceptions')

def clear_local_files():
    """ Delete all files in local directory | None --> None """
    for file in get_local_path().iterdir():
        print('Deleting: ' + str(file))
        file.unlink()

@atexit.register
def cleanup():
    """ Clean up environment on initialization and exit | None --> None

    Presently only runs clear_local_files, but other actions could
    be added as needed, which is why it's a separate function. It is not
    guaranteed to run if program exit occurs while a child process is running,
    but should run often enough to prevent accumulation of unneeded files.
    """
    #Only runs when main process exits with no child processes running
    if not get_child_flag() > 0:
        print('Cleaning up environment')
        clear_local_files()

def insert_lines(readlines_list, index_newline_list):
    """ Insert lines in list of file lines. | [str], [(int, [str])] --> [str]

    Takes file.readlines() output list and a list of tuples of line index
    and corresponding list of lines to insert.
    """
    for tup in index_newline_list:
        index = tup[0]
        lines = tup[1]
        for line in lines:
            readlines_list.insert(index, line)
            index += 1
    return readlines_list

def get_local_filepath(filepath):
    """ Change filepath to local directory, used to copy a file | str -->  Path

    Takes a path in string form, changes the file directory to the local directory,
    then returns a new pathlib.Path object.

    """
    source_path = pathlib.Path(filepath)
    source_name = source_path.name
    new_path = get_local_path().joinpath(source_name)
    return new_path

def create_local_script(filepath):
    """ Create local copy of a script, return the new filepath | str or Path --> Path

    Also makes following changes to script:
    - Changes working directory to original script path to ensure it runs properly
    despite now being run from local directory
    - Adds original script path to sys.path to ensure imports still work
    - Imports web_input and web_print to replace regular input and print calls
    - Writes script finished to prompt file (used for scripts with input calls)

    """
    new_path = get_local_filepath(filepath)
    source_path = pathlib.Path(filepath)
    source_directory = source_path.parent
    SCRIPT_INSERT = ['import os',
                     '\n',
                     'import sys',
                     '\n',
                     'from autofront.input_utilities import web_input, write_prompt',
                     '\n',
                     'from autofront.utilities import web_print',
                     '\n',
                     '__builtins__.input = web_input',
                     '\n',
                     '__builtins__.print = web_print',
                     '\n'
                     'os.chdir("' + str(source_directory.resolve()) + '")',
                     '\n',
                     'sys.path.insert(0, "' + str(source_directory.resolve()) + '")',
                     '\n'
                     ]
    SCRIPT_END = ['\n',
                  'write_prompt("finished")',
                  '\n'
                  ]
    with open(source_path, 'r') as source_script:
        contents = source_script.readlines()
    with open(new_path, 'w') as new_script:
        new_content = insert_lines(contents, [(0, SCRIPT_INSERT)])
        final_content = new_content + SCRIPT_END
        new_script.writelines(final_content)
    return new_path

def clear_display():
    """ Clear display text file | None --> None

    'display.txt' file is where all print calls are redirected
    for display in browser.

    """
    print('Clearing display')
    print('Current status dictionary:')
    print(str(status))
    if status['request_received'] and not status['request_completed']:
        pass
    else:
        with open(get_local_path().joinpath('display.txt'), 'w'):
            pass

def get_display():
    """ Get info from display text file | None --> str

    'display.txt' file is where all print calls are redirected
    for display in browser.

    """
    try:
        with open(get_local_path().joinpath('display.txt'), 'r') as filepath:
            display = filepath.read()
            display = display.split('\n')
        return display
    except FileNotFoundError:
        with open(get_local_path().joinpath('display.txt'), 'w') as filepath:
            return ''

def print_exception(e):
    """ Used by exception_manager to print to browser | None --> None"""
    clear_display()
    with open(get_local_path().joinpath('display.txt'), 'w') as out:
        with contextlib.redirect_stdout(out):
            print(e.__class__.__name__)
            print(e.args[0])

def exception_manager(func):
    """ Decorator to display exceptions in the browser | func --> func

    Used as a decorator to display runtime exception information
    in the browser instead of raising an exception.

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if config['print_exceptions']:
            try:
                wrapped_func = func(*args, **kwargs)
            except Exception as e:
                wrapped_func = None
                print_exception(e)
        else:
            wrapped_func = func(*args, **kwargs)
        return wrapped_func
    return wrapper

def web_print(*args, file=None, end='\n', sep=' ', flush='Unsupported'):
    """ Replaces the built-in print function to write to file | str --> None

    Ignores the flush kwarg.
    See builtin print function docs for explanation of the sep and end kwargs.
    Behavior should be similar to builtin print function.

    """
    if file:
        for arg in args:
            file.write(str(arg))
            file.write(sep)
        file.write(end)
    else:
        with open(get_local_path().joinpath('display.txt'), 'a') as display_file:
            for arg in args:
                display_file.write(str(arg))
                display_file.write(' ') #NOTE - Extra space after final arg
            display_file.write(end)

def redirect_print(func):
    """ Decorator to divert print calls to the browser | func --> func

    Used as a decorator to print to 'display.txt' for display
    in the browser instead of to the console.

    """
    @functools.wraps(func)
    @exception_manager
    def wrapper(*args, **kwargs):
        bkup_print = __builtins__['print']
        __builtins__['print'] = web_print
        try:
            return_value = func(*args, **kwargs)
        finally:
            __builtins__['print'] = bkup_print
        return return_value
    return wrapper

@redirect_print
def print_to_display(string):
    """ Prints any string to the display text_file | str --> None

    'display.txt' file is used to display text in the browser.

    """
    print(string)

def print_return_value(return_value):
    """ Prints the return value of a function to display file | any --> None

    'display.txt' file is used to display text in the browser.

    """
    if return_value:
        return_string = str(return_value)
        intro = 'Return value: '
        print_to_display(intro + return_string)

def wrap_script(script_path, *args):
    """ Create function to run script | Path, [str] --> func

    Returns a function that will run a script using the subprocess module.
    """
    command_list = list(args)
    command_list.insert(0, script_path.resolve())
    command_list.insert(0, 'python3')
    def new_function():
        with open(get_local_path().joinpath('display.txt'), 'a') as out:
            subprocess.run(command_list, stdout=out, check=True)
    new_function.__name__ = script_path.name
    return new_function

def add_args_to_title(route_title, arg_list, script=False):
    """ Add fixed args to function name for display in browser | str, [str] --> str """
    title = route_title
    if not script:
        title += ' ('
    if arg_list:
        title += ' '
        title += ', '.join(arg_list)
        title += ','
    return title

def title_exists(title):
    """ Check if a route with this title already exists | str --> Bool """
    route_dict = [route_dict for route_dict in config['route_dicts']
                  if route_dict['title'] == title]
    if route_dict:
        return True
    return False

def get_route_dict(title):
    """ Get specific route dict from route_dicts | str --> dict """
    route_dict = [route_dict for route_dict in config['route_dicts']
                  if route_dict['title'] == title]
    if len(route_dict) > 1: #Shouldn't happen, here for safety
        raise Exception('Cannot use same title twice')
    try:
        route_dict = route_dict[0]
    except IndexError:
        print(title)
        print(str(route_dict))
        raise IndexError("Couldn't find route dict with this title")
    return route_dict

def get_fixed_args(title):
    """ Get fixed args for a function from route_dicts | str --> [[str],[str]]"""
    route_dict = get_route_dict(title)
    all_fixed_args = []
    fixed_args = route_dict['args'].copy()
    fixed_kwargs = route_dict['kwargs'].copy()
    all_fixed_args = [fixed_args, fixed_kwargs]
    return all_fixed_args

def get_function(title):
    """ Get function from route_dicts | str --> func"""
    route_dict = get_route_dict(title)
    function = route_dict['function']
    return function

def get_script_path(title):
    """ Get script_path from route_dicts | str --> str"""
    route_dict = get_route_dict(title)
    script_path = route_dict['script_path']
    return script_path

def is_script(title):
    """ Check if route is for a script | str --> bool"""
    route_dict = get_route_dict(title)
    bool_value = route_dict['script']
    return bool_value

def is_live(title):
    """ Check if script or function needs live arguments | str --> bool """
    route_dict = get_route_dict(title)
    bool_value = route_dict['live']
    return bool_value

def has_key(title, key):
    """ Check if route dict has a specific key | str, str --> bool """
    route_dict = get_route_dict(title)
    return key in route_dict

def needs_input(title):
    """ Check if script or function needs user input | str --> bool """
    route_dict = get_route_dict(title)
    bool_value = route_dict['input_call']
    return bool_value

def wait_to_join(title):
    """ Check if script or function needs to keep running | str --> bool

    This is used for functions or scripts that are meant to keep running
    in background.

    """
    route_dict = get_route_dict(title)
    bool_value = route_dict['join']
    return bool_value

def get_timeout(title):
    """ Get timeout value of function or script | str --> bool """
    route_dict = get_route_dict(title)
    timeout = route_dict['timeout']
    return timeout

def typed_args(title):
    """ Check if function uses type indications | str --> bool"""
    route_dict = get_route_dict(title)
    bool_value = route_dict['typed']
    return bool_value

def get_live_args(request, typed=False):
    """ Get live args input by user | request --> [[str], [str]]"""
    arg_string = list(request.form.values())[0]
    if typed:
        all_args = parse_type_args(arg_string)
    else:
        all_args = parse_args(arg_string)
    args = all_args[0]
    kwargs = all_args[1]
    all_args = [args, kwargs]
    return all_args

def print_route_dicts():
    """ Print all route dicts with pretty print | None --> None

    This is used for development purposes to make sure route_dicts
    are behaving properly.

    """
    for route_dict in config['route_dicts']:
        pprint.pprint(route_dict)
