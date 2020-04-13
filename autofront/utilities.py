import contextlib, datetime, sys, pathlib, string, subprocess, functools
from flask import Flask

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

def strip_surrounding_spaces(input):
    if input[0] == ' ':
        input = input[1:]
    if input[-1] == ' ':
        input = input[:-1]
    return input

def parse_kwargs(kwarg_list):
    kwargs = {}
    for kwarg in kwarg_list:
        key_value = kwarg.split('=')
        key = key_value[0]
        key = strip_surrounding_spaces(key)
        value = key_value[1]
        value = strip_surrounding_spaces(value)
        kwargs[key] = value
    return kwargs

def parse_args(arg_string):
    arg_string = strip_surrounding_spaces(arg_string)
    arg_list = arg_string.split(sep=',')
    args = []
    kwargs = []
    for arg in arg_list:
        if '=' in arg:
            kwargs.append(arg)
        else:
            args.append(arg)
    
    kwargs = parse_kwargs(kwargs)
    all_args = [args, kwargs]
    return all_args

def get_args(request, func_name, func_dicts):
    arg_string = list(request.form.values())[0]
    all_args = parse_args(arg_string)
    print('live all args: ' + str(all_args))
    args = all_args[0]
    print('live args: ' + str(args))
    kwargs = all_args[1]
    print('live kwargs: ' + str(kwargs))
    all_args = [args, kwargs]
    print('combined_args: ' + str(all_args))
    return all_args


def parse_bool(arg):
    if arg == 'True':
        return True
    elif arg == 'False':
        return False
    else:
        print('Your arg was: ' + arg)
        raise ValueError('Correct format for boolean type is ' +
                         '"bool:True" or "bool:False"')

def parse_string(arg):
    return arg

def parse_int(arg):
    return int(arg)

def parse_float(arg):
    return float(arg)

def parse_complex(arg):
    return complex(arg)

def parse_list(arg):
    temp_list = arg.strip('[]').split(',')
    parsed_list = parse_type_args(temp_list)
    return parsed_list

def get_list_indexes(arg_string):
    list_starts = [index for index, char in enumerate(arg_string)
                  if char == '[']
    list_ends = [index for index, char in enumerate(arg_string)
                  if char == ']']
    list_indexes = list(zip(list_starts, list_ends))
    return list_indexes

def list_ranges(arg_string):
    list_indexes = get_list_indexes(arg_string)
    list_ranges = []
    for indexes in list_indexes:
        list_ranges += list(range(indexes[0],indexes[1]))
    return list_ranges

def get_colon_indexes(arg_string):
    colon_list = [index for index, char in enumerate(arg_string)
                  if char == ':']
    return colon_list

def split_indexes(arg_string):
    split_list = []
    colon_indexes = get_colon_indexes(arg_string)
    list_indexes = list_ranges(arg_string)
    for colon in colon_indexes[1:]:
        if colon not in list_indexes:
            split_list.append(arg_string.rfind(',', 0, colon))
    return split_list

def split_type_args(arg_string):
    split_list = split_indexes(arg_string)
    arg_list = []
    start = 0
    for index in split_list:
        arg_list.append(arg_string[start:index])
        start = index + 1
        while arg_string[start] == ' ':
            start += 1
    arg_list.append(arg_string[start:len(arg_string)])
    return arg_list
        
parsing_functions = {'bool' : parse_bool,
                     'str' : parse_string,
                     'int' : parse_int,
                     'float' : parse_float,
                     'complex' : parse_complex,
                     'list' : parse_list}

def parse_type_args(arg_list):
    parsed_list = []
    for arg in arg_list:
        type_arg = arg.partition(':')
        type = type_arg[0].strip(' ')
        arg = type_arg[2]
        parsed_list.append(parsing_functions[type](arg))
    return parsed_list

