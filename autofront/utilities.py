import contextlib, datetime, sys, pathlib, string, subprocess, functools
from flask import Flask
from autofront.parse import parse_args, parse_type_args

print_exceptions = True

def raise_exceptions():
    global print_exceptions
    print_exceptions = not print_exceptions
    
def initialize(name):
    clear_display()
    app = Flask(name)
    return app

display_path = str(pathlib.Path(__file__).parent)

def clear_display():
    with open(display_path + '/display.txt', 'w') as out:
        pass

def get_display():
    with open(display_path + '/display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return display

"""
Used as a decorator to print to a file for display
in the browser instead of to the console.
If using multiprocessing, it's essential to add "sys.stdout.flush()"
after the print calls in your child process, otherwise the file
will only be written on program exit. Otherwise,
your original function should not need any modification.
"""

def redirect_print(func):
    @functools.wraps(func)
    @exception_manager
    def wrapper(*args, **kwargs):
        with open(display_path + '/display.txt', 'a') as out:
            print('Display path: ' + display_path)
            with contextlib.redirect_stdout(out):
                #print(datetime.datetime.now()) #Uncomment for debugging
                #print(func.__name__) #Uncomment for debugging
                wrapped_func = func(*args, **kwargs)
                return wrapped_func
    return wrapper

def print_exception(e):
    clear_display()
    with open(display_path + '/display.txt', 'w') as out:
        with contextlib.redirect_stdout(out):
            print(e.__class__.__name__)
            print(e.args[0])

"""
Used as a decorator to display runtime exception information
in the browser instead of raising an exception. Change boolean value
of print_exceptions to turn on or off. You can also add raise_exceptions
to your routes to switch this functionality on or off for all your routes.
"""

def exception_manager(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if print_exceptions:
            try:
                wrapped_func = func(*args, **kwargs)
            except Exception as e:
                wrapped_func = print_exception(e)
        else:
            wrapped_func = func(*args, **kwargs)
        return wrapped_func
    return wrapper


def run_script(script, *args):
    print('running ' + script)
    script_path = './' + script
    command_list = list(args)
    command_list.insert(0, script_path)
    command_list.insert(0, 'python')
    print(command_list)
    def new_function():
        with open(display_path + '/display.txt', 'a') as out:
            subprocess.run(command_list, stdout = out)
    new_function.__name__ = script
    return new_function


def add_args_to_title(func_name, arg_list):
    title = func_name + ' ('
    if arg_list:
        title += ' ' 
        title += ', '.join(arg_list)
        title += ','
    return title

def get_func_dict(func_title, func_dicts):
    func_dict = [func_dict for func_dict in func_dicts
                 if func_dict['title'] == func_title]
    if len(func_dict) > 1:
        raise Exception('Cannot use same title for your functions')
    else:
        func_dict = func_dict[0]
    return func_dict

def get_fixed_args(func_name, func_dicts):
    func_dict = get_func_dict(func_name, func_dicts)
    all_fixed_args = []
    fixed_args = func_dict['args']
    fixed_kwargs = func_dict['kwargs']
    all_fixed_args = [fixed_args, fixed_kwargs]
    return all_fixed_args

def get_function(func_title, func_dicts):
    func_dict = get_func_dict(func_title, func_dicts)
    function = func_dict['func']
    return function

def live_script(func_title, func_dicts):
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['script'] and func_dict['live']
    return bool_value

def type_args(func_title, func_dicts):
    func_dict = get_func_dict(func_title, func_dicts)
    bool_value = func_dict['type']
    return bool_value

def get_args(request, func_name, func_dicts, type = False):
    arg_string = list(request.form.values())[0]
    if type:
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
