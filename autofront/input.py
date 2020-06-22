import time
from autofront.utilities import get_local_path, get_func_dict, get_display

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

def write_input(string):
    """ Write string to input text file | str --> None """
    with open(get_local_path().joinpath('input.txt'), 'w') as input_file:
        input_file.write(string)
    
def clear_input():
    """ Clear input text file | None --> None """
    with open(get_local_path().joinpath('input.txt'), 'w'):
        pass

def put_input_args(func_title, func_dicts, arg_list):
    """ Store args for function with input call | str, dict --> None
    
    Temporarily stores the args for a script using input calls in func dict.
    Will be deleted when script has finished execution.

    """
    func_dict = get_func_dict(func_title, func_dicts)
    func_dict['input_args'] = arg_list

def get_input_args(func_title, func_dicts):
    """ Get args for a script with input calls | str, dict --> list

    This dict key only exists while input script is being executed.
    It will fail if called on any other script or at any other time.

    """
    func_dict = get_func_dict(func_title, func_dicts)
    input_args = func_dict['input_args']
    return input_args

def wait_for_prompt(timeout=0):
    """ Waits for prompt file to be written and returns contents | None --> str
        
        If script does not end after seconds specified in 'timeout' kwarg,
        will return 'timeout reached'.

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
                print('sleeping')
                print('prompt: ' + get_prompt())
                print('input: ' + get_input())
                print('display: ' + str(get_display()))
                time.sleep(1)
                if timeout: #if timeout 0, time_waited will never increase
                    time_waited += 1
            else:                
                prompt_received=True

def wait_for_input():
    """ Waits for input file to be written, then returns True | None --> str """
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
    Browser input gets user input in browser and writes to input file.
    Reads input file and returns it just as for original input call.
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
    return input_received

def redirect_input(func):
    """ Decorator to divert input calls to the browser | func --> func"""
    @functools.wraps(func)
    @exception_manager
    def wrapper(*args, **kwargs):
        bkup_input = __builtins__['input']
        __builtins__['input'] = web_input
        return_value = func(*args, **kwargs)
        __builtins__['input'] = bkup_input
        return return_value
    return wrapper
