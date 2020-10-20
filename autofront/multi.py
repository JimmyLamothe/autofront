""" Multiprocessing worker module
This module is used to create workers that run the scripts and functions designated
in autofront.create_route using the multiprocessing module. There are different
workers for running scripts, regular functions, and functions that use input calls.

'worker_dicts' stores all worker dictionaries
'create_process' is the main function used to create workers.
'cleanup_workers' removes dead workers from worker_dicts and any workers above
the worker limit value set in config.py.
'info', 'kill' and 'kill_all'  are used for testing purposes during development.
"""

import multiprocessing
import time
from autofront.config import config, status
from autofront.input_utilities import redirect_input
from autofront.utilities import print_return_value, print_to_display
from autofront.utilities import redirect_print, wrap_script

worker_dicts = []
""" Worker_dict keys:
'worker': process - this is the actual worker
'start_time': process start time
'timeout': maximum allowed running time. Set to None if no timeout limit.
"""

def script_worker(script_path, *args):
    """ Process target for scripts | func, args, kwargs --> None """
    wrapped_script = wrap_script(script_path, *args)
    wrapped_script()


@redirect_print
def function_worker(function, *args, **kwargs):
    """ Process target for regular functions | func, args, kwargs --> None """
    print_return_value(function(*args, **kwargs))

@redirect_print
@redirect_input
def input_worker(function, *args, **kwargs):
    """ Process target for input functions | func, args, kwargs --> None """
    print_return_value(function(*args, **kwargs))

def get_running_time(worker_dict):
    """ How long a worker has been running | dict --> float """
    current_time = time.time()
    start_time = worker_dict['start_time']
    running_time = current_time - start_time
    return running_time

def create_process(function_or_script_path, *args, type=None, join=True,
                   timeout=None, **kwargs):
    """ Main function used to create workers | func, args, kwargs --> None

    Creates a worker (multiprocessing.Process object) and starts it. This is how
    all routes actually run functions.

    'type' should always be specified and determines which function to target

    Set 'join' to False if function needs to keep running in background.
    This is automatic for functions using input calls.

    In this case, a worker_dict will be created with the actual worker,
    start_time and timeout values and stored in worker_dicts.
    The worker will keep running until function ends normally or timeout expires.

    If a function or script is hanging, the timeout kwarg can be used
    to force stop it and allow the server to keep running.
    """
    if status['waiting']:
        print('Waiting for route to finish execution, ignoring user input')
        return
    type_dict = {'script':script_worker,
                 'function':function_worker,
                 'input':input_worker}
    target = type_dict[type] #Get correct function for process type
    if type == 'script':
        script_path = function_or_script_path
        name = script_path.name
        args = tuple([script_path] + list(args))
    else:
        function = function_or_script_path
        name = function.__name__
        args = tuple([function] + list(args))
    start_time = time.time()
    worker = multiprocessing.Process(target=target, name=name, args=args,
                                     kwargs=kwargs)
    worker.start()
    worker_dict = {'worker':worker,
                   'start_time':start_time,
                   'timeout':timeout}
    worker_dicts.append(worker_dict)
    if join: #For normal functions that need to finish running
        print('Waiting for {} to finish'.format(worker.name))
        status['waiting'] = True
        worker.join(timeout=timeout)
        if worker.is_alive():
            print('{} timed out, killing process'.format(worker.name))
            error_message = '{} timed out before completion.\n'.format(worker.name)
            error_message += 'You can change the timeout value with a kwarg:\n'
            error_message += 'autofront.create_route(my_function, '
            error_message += 'timeout=value_in_seconds)'
            if config['print_exceptions']:
                print_to_display(error_message)
            else:
                print(error_message)
            kill(worker)
        else:
            print('{} finished normally'.format(worker.name))
        status['waiting'] = False
    status['request_completed'] = True

def is_alive(worker_dict):
    """ Test if worker is alive and running | None --> Bool """
    return worker_dict['worker'].is_alive()

def timeout_expired(worker_dict):
    """ Test if timeout value has been reached | None --> Bool """
    timeout = worker_dict['timeout']
    if timeout:
        return get_running_time(worker_dict) > worker_dict['timeout']
    return False

def timeout_okay(worker_dict):
    """ Tests if timeout value has not been reached yet | None --> Bool """
    return not timeout_expired(worker_dict)

def cleanup_workers():
    """ Remove dead and timed out workers from worker_dicts | None --> None """
    #info() #Uncomment for development and debugging
    global worker_dicts
    print('Removing dead processes if any')
    worker_dicts = list(filter(is_alive, worker_dicts))
    print('Removing processes still running past timeout if any')
    for worker_dict in filter(timeout_expired, worker_dicts):
        print('Removing dead workers')
        try:
            kill(worker_dict['worker'])
        except RuntimeError:
            print('Failed to kill {}'.format(worker_dict['worker'].name))
    worker_dicts = list(filter(timeout_okay, worker_dicts))
    limit = config['worker_limit']
    if limit:
        while len(worker_dicts) > limit:
            print('Too many workers, ending oldest process')
            try:
                kill(worker_dicts[0]['worker'])
                worker_dicts.pop(0)
            except RuntimeError:
                print('Failed to kill {}'.format(worker_dicts[0]['worker'].name))
    #info() #Uncomment for development and debugging

def kill(worker):
    """ Terminate a worker process | obj --> None """
    print('Killing worker {}'.format(worker.name))
    worker.terminate()
    time.sleep(0.5)
    if not worker.is_alive():
        print('Worker {0} was terminated'.format(worker.name))
    else:
        raise RuntimeError('Failed to kill process')

def kill_all():
    """ Terminate all processes in worker_dicts | None --> None

    Used for testing in development.
    """
    print('Killing all processes')
    for worker_dict in worker_dicts:
        worker = worker_dict['worker']
        kill(worker)

def info():
    """ Get info on processes in worker_dicts | None --> None """
    for index, worker_dict in enumerate(worker_dicts):
        worker = worker_dict['worker']
        print('Worker #{0}: {1}'.format(str(index), worker.name))
        running_time = str(get_running_time(worker_dict))
        dot_index = running_time.find('.')
        print('Running time: {}'.format(running_time[0:dot_index]))
        print('Currently alive: {}'.format(str(worker.is_alive())))
        timeout = worker_dict['timeout']
        if timeout:
            print('Maximum worker time: {}'.format(str(timeout)))
    print('{} workers in queue'.format(len(worker_dicts)))
    limit = config['worker_limit']
    if limit:
        print('Maximum of {} workers allowed'.format(str(limit)))
