import time
import multiprocessing
from autofront.utilities import get_local_path, get_func_dict

def initialize_prompt():
    """ Initialize prompt file on script start | None --> None """
    with open(get_local_path().joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write('waiting for prompt')

def get_prompt():
    """ Get contents of prompt text file | None --> str """
    with open(get_local_path().joinpath('prompt.txt'), 'r') as prompt_file:
        return prompt_file.read()

def initialize_input():
    """ Initialize input file on script start | None --> None """
    with open(get_local_path().joinpath('input.txt'), 'w') as input_file:
        input_file.write('waiting for input')

def get_input():
    """ Get contents of input text file | None --> str """
    with open(get_local_path().joinpath('input.txt'), 'r') as input_file:
        return input_file.read()

def clear_prompt():
    """ Clear prompt text file | None --> None """
    with open(get_local_path().joinpath('prompt.txt'), 'w'):
        pass

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

def web_input(prompt):
    """ Replaces the built-in input function for browser input | str --> str 
    
    Writes input prompt to prompt file to activate browser_input.
    Browser input gets user input in browser and writes to input file.
    Reads input file and returns it just as for original input call.
    """
    clear_input()
    input_received = False
    with open(get_local_path().joinpath('prompt.txt'), 'w') as prompt_file:
        prompt_file.write(prompt)
    while not input_received:
        with open(get_local_path().joinpath('input.txt'), 'r') as input_file:
            contents = input_file.read()
            if not contents:
                time.sleep(1)
            else:
                input_received=True
                return contents

def wait_for_prompt():
    """ Waits for prompt file to be written and returns contents | None --> str """
    clear_prompt()
    prompt_received = False
    while not prompt_received:
        with open(get_local_path().joinpath('prompt.txt'), 'r') as prompt_file:
            if not prompt_file.read():
                time.sleep(1)
            else:
                prompt_received=True
                return prompt_file.read()

def start_process(function, *args, **kwargs):
    process = multiprocessing.Process(target = function, args = [*args],
                                      kwargs = {**kwargs})
    #process.daemon = True
    process.start()
    print('Running processes: ' + str(count_mp_children()))
    process.join()

def count_mp_children():
    active_processes = multiprocessing.active_children()
    mp_warning()
    return len(active_processes)

def stop_queue():
    for process in multiprocessing.active_children():
        process.terminate()
        self.mp_warning()

def mp_warning():
    active_processes = multiprocessing.active_children()
    if len(active_processes) > 2:
        print('Warning: unusually high number of active processes')
    if len(active_processes) > 10:
        stop_queue()
    if len(active_processes) > 10:
        error_message = 'Critical failure: too many active processes, ' 
        error_message += 'debugging neccessary'
        raise MemoryError(error_message)

