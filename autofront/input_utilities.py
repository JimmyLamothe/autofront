""" Module enabling functions and scripts with input calls

The builtin input function needs to be replaced to get input in the browser instead
of in the console. This module enables this functionality. Since the server and
the function or script are running in separate processes, they communicate by writing
to the prompt.txt and input.txt files.

When an input script or function is detected, autofront.browser_input starts
the process and waits for the prompt file to be written.

web_input replaces the builtin input function inside the process.
It writes the prompt to the prompt file and waits for input.

autofront.browser_input reads the prompt file and gets user input in the browser.
It writes the input to the input file.

web_input read the input from the input file and returns it.

redirect_input is a decorator enabling functions to be run with web_input instead
of the builtin input function.

"""

import functools
import time
from autofront.utilities import get_local_path, get_route_dict, get_display, has_key
from autofront.utilities import exception_manager

def initialize_prompt():
    """ Initialize prompt file on script start | None --> None """
    with open(get_local_path().joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write('waiting for prompt')

def get_prompt():
    """ Get contents of prompt text file | None --> str """
    with open(get_local_path().joinpath('prompt.txt'), 'r') as prompt_file:
        return prompt_file.read()

def write_prompt(string):
    """ Write string to prompt text file | str --> None """
    with open(get_local_path().joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write(string)

def clear_prompt():
    """ Clear prompt text file | None --> None """
    with open(get_local_path().joinpath('prompt.txt'), 'w'):
        pass

def initialize_input():
    """ Initialize input file on script start | None --> None """
    with open(get_local_path().joinpath('input.txt'), 'w') as input_file:
        input_file.write('waiting for input')

def get_input():
    """ Get contents of input text file | None --> str """
    with open(get_local_path().joinpath('input.txt'), 'r') as input_file:
        return input_file.read()

def get_timeout(title):
    """ Get timeout delay from route_dicts | str --> int """
    route_dict = get_route_dict(title)
    timeout = route_dict['timeout']
    return timeout

def write_input(string):
    """ Write string to input text file | str --> None """
    with open(get_local_path().joinpath('input.txt'), 'w') as input_file:
        if string:
            input_file.write(string)
        else:
            input_file.write('**BLANK_INPUT_RECEIVED**')

def clear_input():
    """ Clear input text file | None --> None """
    with open(get_local_path().joinpath('input.txt'), 'w'):
        pass

def put_input_args(title, args, kwargs=None):
    """ Store args for function with input call | str, dict --> None

    Temporarily stores the args for a script using input calls in func dict.
    Will be deleted when script has finished execution.

    """
    route_dict = get_route_dict(title)
    route_dict['input_args'] = args
    if kwargs:
        route_dict['input_kwargs'] = kwargs

def get_input_args(title):
    """ Get args for a script with input calls | str, dict --> list """
    route_dict = get_route_dict(title)
    input_args = route_dict['input_args']
    return input_args

def get_input_kwargs(title):
    """ get kwargs for a script with input calls | str, dict --> dict """
    if has_key(title, 'input_kwargs'):
        route_dict = get_route_dict(title)
        return route_dict['input_kwargs']
    return {}

def wait_for_prompt(timeout=0):
    """ Wait for prompt file to be written | None --> None

        If script does not end after seconds specified in 'timeout' kwarg,
        will write 'timeout reached' to prompt file.

    """
    clear_prompt()
    prompt_received = False
    time_waited = 0
    while not prompt_received or time_waited > timeout:
        with open(get_local_path().joinpath('prompt.txt'), 'r') as prompt_file:
            contents = prompt_file.read()
            if time_waited > timeout:
                write_prompt('timeout reached')
                break
            if not contents:
                print('Waiting_for_prompt')
                time.sleep(1)
                if timeout: #if timeout 0, time_waited will never increase
                    time_waited += 1
            else:
                print('Prompt received')
                prompt_received = True

def wait_for_input():
    """ Wait for input file to be written, then returns contents | None --> str """
    clear_input()
    input_received = False
    while not input_received:
        with open(get_local_path().joinpath('input.txt'), 'r') as input_file:
            contents = input_file.read()
            if not contents:
                time.sleep(1)
            else:
                return contents

def web_input(*args):
    """ Replaces the built-in input function for browser input | str --> str

    Writes input prompt to prompt file to activate browser_input.
    autofront.browser_input gets user input in browser and writes to input file.
    Reads input file and returns contents.
    """
    if args:
        prompt = [*args][0]
    else:
        prompt = 'None'
    clear_input()
    input_received = False
    with open(get_local_path().joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write(prompt)
    while not input_received:
        input_received = wait_for_input() #Returns contents when received
    if input_received == '**BLANK_INPUT_RECEIVED**':
        return ''
    return input_received

def redirect_input(func):
    """ Decorator to divert input calls to the browser | func --> func"""
    @functools.wraps(func)
    @exception_manager
    def wrapper(*args, **kwargs):
        bkup_input = __builtins__['input']
        __builtins__['input'] = web_input
        try:
            return_value = func(*args, **kwargs)
        finally:
            __builtins__['input'] = bkup_input
            write_prompt('finished')
        return return_value
    return wrapper
