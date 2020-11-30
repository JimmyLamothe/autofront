""" Utility functions


This module contains various functions that help create routes
and process user input for live arguments. It calls on the parse module
to parse arguments with type indications.

"""

import atexit
import contextlib
import functools
import multiprocessing
import pathlib
import pprint
import shutil
import socket
import subprocess
from autofront.config import config, status
from autofront.parse import parse_command_line_args, parse_args, parse_type_args

def create_local_dir():
    """ Creates local directory if it doesn't exist | None --> None """
    pathlib.Path(__file__).parent.joinpath('local').mkdir(exist_ok=True)

def get_local_path():
    """ Get local path | None --> Path

    The local path is where all temporary files are created.
    They are deleted on program exit.
    """
    return pathlib.Path(__file__).parent.joinpath('local')

def local_read(filename):
    """ Open a file in local directory | str --> str """
    with open(get_local_path().joinpath(filename), 'r') as file_object:
        return file_object.read()

def local_write(filename, string):
    """ Write to a file in local directory | str, str --> None """
    with open(get_local_path().joinpath(filename), 'w') as file_object:
        file_object.write(string)

def get_shell_python_version(command='python -V'):
    """ Get version of Python running in shell | None --> tuple

    Use command keyword to test python3 instead of python
    if python version is Python 2.

    Minor version is not used at present but is included in case it is needed
    in future versions.
    """
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, check=True,
                            stderr=subprocess.STDOUT, universal_newlines=True)
    version_string = result.stdout
    major_version_index = version_string.find(' ') + 1
    major_version = int(version_string[major_version_index])
    minor_version_index = version_string.find('.') + 1
    minor_version = int(version_string[minor_version_index])
    micro_version_index = version_string.rfind('.') +1
    end_index = len(version_string)
    micro_version = int(version_string[micro_version_index:end_index])
    return tuple([major_version, minor_version, micro_version])

def set_python_command():
    """ Set python command to run scripts in the shell | None --> None

    Finds the correct command to run Python 3.
    Tests "python" first, then "python3" if "python" runs Python 2.
    """
    print('Testing "python" command')
    version = get_shell_python_version()
    major_version = version[0]
    minor_version = version[1]
    micro_version = version[2]
    if major_version == 2:
        print('Testing "python3" command')
        try:
            version = get_shell_python_version(command='python3 -V')
            major_version = version[0]
            minor_version = version[1]
            micro_version = version[2]
            if major_version == 3:
                print('Scripts will be run with "python3" command')
                print('Python version is {0}.{1}.{2}'.format(major_version,
                                                             minor_version,
                                                             micro_version))
                local_write('python_command.txt', 'python3')
            else:
                print('Error identifying correct python command to run scripts.')
                print("Defaulting to 'python'")
        except IndexError:
            print('Warning: Your script environment is in Python 2.')
            print('Scripts will be run using the Python 2 interpreter')
            print('This will probably fail due to incompatibilities with autofront')
            print('Shell Python version is {0}.{1}.{2}'.format(major_version,
                                                               minor_version,
                                                               micro_version))
    else:
        print('Scripts will be run with "python" command')
        print('Python version is {0}.{1}.{2}'.format(major_version,
                                                     minor_version,
                                                     micro_version))
        local_write('python_command.txt', 'python')

def get_python_command():
    """ Get correct version of python command | None --> str """
    return local_read('python_command.txt')

def set_main_process_pid():
    """ Store main process pid | None --> None

    Note: This function simply stores the current process id. Its name
    is meant to clarify the fact that it's always called in the main process
    to identify it. If it were called in a child process it would return
    the child process id.
    """
    main_process_pid = multiprocessing.current_process().pid
    local_write('main_process_pid.txt', str(main_process_pid))

def get_main_process_pid():
    """ Get main process pid | None --> str """
    return int(local_read('main_process_pid.txt'))

def get_current_process_pid():
    """ Get current process pid | None --> str """
    current_process_pid = multiprocessing.current_process().pid
    return current_process_pid

def check_for_main():
    """ Returns false if not in main process | None --> Bool

    This check replaces the standard if __name__ == '__main__' used
    with the multiprocessing module to prevent child processes from
    running functions when they import the main module.
    """
    try:
        if get_current_process_pid() == get_main_process_pid():
            return True
        return False
    except FileNotFoundError:
        return True

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
    """ Delete all files in local directory | None --> None

    If autofront returns without doing anything, this might be because
    main_process_pid.txt has not been properly deleted on program exit
    (in case of a power failure, for example. If this is the  case,
    start up a python shell, import autofront and run::
        autofront.utilities.clear_local_files()
    """
    for path in get_local_path().iterdir():
        print('Deleting: ' + str(path))
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

@atexit.register
def cleanup():
    """ Clean up environment on initialization and exit | None --> None

    Presently only runs clear_local_files, but other actions could
    be added as needed, which is why it's a separate function.
    """
    if check_for_main():
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

def clear_display():
    """ Clear display text file | None --> None

    'display.txt' file is where all print calls are redirected
    for display in browser.
    """
    print('Clearing display')
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
            print(e.__class__.__name__ + ': ' + e.args[0])

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
    if file: #For compatibility with builtin print kwargs
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

def create_local_script(filepath):
    """ Create local copy of a script, return the new filepath | str or Path --> Path

    Also makes following changes to script:
    - Changes working directory to original script path to ensure it runs properly
    despite now being run from local directory
    - Adds original script path to sys.path to ensure imports still work
    - Imports web_input and web_print to replace regular input and print calls
    """
    new_path = get_local_filepath(filepath)
    source_path = pathlib.Path(filepath)
    source_directory = source_path.parent
    SCRIPT_INSERT = ['import os',
                     '\n',
                     'import sys',
                     '\n'
                     'from autofront.utilities import web_print',
                     '\n',
                     'from autofront.input_utilities import web_input, write_prompt',
                     '\n',
                     '__builtins__.input = web_input',
                     '\n',
                     '__builtins__.print = web_print',
                     '\n',
                     'os.chdir(r"' + str(source_directory.resolve()) + '")',
                     '\n',
                     'sys.path.insert(0, r"' + str(source_directory.resolve()) + '")',
                     '\n'
                     ]
    with open(source_path, 'r') as source_script:
        contents = source_script.readlines()
    with open(new_path, 'w') as new_script:
        new_content = insert_lines(contents, [(0, SCRIPT_INSERT)])
        new_script.writelines(new_content)
    return new_path

def wrap_script(script_path, *args):
    """ Create function to run script | Path, [str] --> func

    Returns a function that will run a script using the subprocess module.
    """
    command_list = list(args)
    command_list.insert(0, str(script_path.resolve()))
    command_list.insert(0, get_python_command())
    def new_function():
        with open(get_local_path().joinpath('display.txt'), 'a') as out:
            subprocess.run(command_list, stdout=out, stderr=out, check=True)
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

def remove_args(route_title):
    """ Remove args from title string for display in console | str --> str """
    print('Running remove_args')
    arg_index = route_title.find('(')
    if arg_index == -1:
        return route_title
    return route_title[0:arg_index]

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
    bool_value = route_dict['input']
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
    if not timeout:
        timeout = config['timeout']
    return timeout

def typed_args(title):
    """ Check if function uses type indications | str --> bool"""
    route_dict = get_route_dict(title)
    bool_value = route_dict['typed']
    return bool_value

def get_live_args(request, script=False, typed=False):
    """ Get live args input by user | request --> [[str], [str]]"""
    arg_string = list(request.form.values())[0]
    if script:
        return parse_command_line_args(arg_string)
    if typed:
        try:
            all_args = parse_type_args(arg_string)
        except Exception as e: #Doesn't matter what the exception is.
            #raise e #Uncomment for testing
            return ('Parsing Error', e)
    else:
        all_args = parse_args(arg_string)
    args = all_args[0]
    kwargs = all_args[1]
    all_args = [args, kwargs]
    print(all_args)
    return all_args

def print_route_dicts():
    """ Print all route dicts with pretty print | None --> None

    This is used for development purposes to make sure route_dicts
    are behaving properly.
    """
    for route_dict in config['route_dicts']:
        pprint.pprint(route_dict)

def get_local_ip():
    """ Get local ip of machine running autofront | None --> str """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname) #For MacOS + Windows
    if local_ip == '127.0.1.1': #For some Linux OS
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    return local_ip
