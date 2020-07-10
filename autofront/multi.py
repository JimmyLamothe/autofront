""" Multiprocessing worker module
This module is used to create workers that run the scripts and functions designated
in autofront.create_route using the multiprocessing module. There are different
workers for running scripts, normal functions and functions that can use input calls.

'worker_dicts' stores all worker dictionaries
'create_process' is the main function used to create workers.
'cleanup_workers' removes dead workers from worker_dicts and any workers above
the worker limit value set in config.py.
'info', 'kill' and 'kill_all'  are used for testing purposes during development.

"""

import multiprocessing
import time
from autofront.config import config
from autofront.input_utilities import redirect_input
from autofront.utilities import redirect_print, put_script_flag, delete_script_flag

status = {'waiting':False}

worker_dicts = []
""" Worker_dict keys:
'worker': process - this is the actual worker
'start_time': process start time
'timeout': maximum allowed running time. Set to None if no timeout limit.
"""

def script_worker(function, *args, **kwargs):
    """ Process target for scripts | func, args, kwargs --> None """
    put_script_flag() #To prevent atexit functions from running early
    function(*args, **kwargs)
    delete_script_flag()

@redirect_print
def function_worker(function, *args, **kwargs):
    """ Process target for regular functions | func, args, kwargs --> None """
    return_value = function(*args, **kwargs)
    if return_value:
        print(return_value)

@redirect_print
@redirect_input
def input_worker(function, *args, **kwargs):
    """ Process target for input functions | func, args, kwargs --> None """
    return_value = function(*args, **kwargs)
    if return_value:
        print(return_value)

def get_running_time(worker_dict):
    """ How long has a worker been running | dict --> float """
    current_time = time.time()
    start_time = worker_dict['start_time']
    running_time = current_time - start_time
    return running_time

def test_for_main():
    """ Test if __name__ == '__main__' | None --> Bool

    Was used for development purposes to see if extra processes were being created.
    In autofront's case, __name__ is actually 'autofront.multi' instead of '__main__',
    but no extra processes are created.
    """
    if __name__ == '__main__':
        return True
    print('Name is {} instead of __main__'.format(__name__))
    return False

def test_for_multi():
    """ Test if __name__ == 'autofront.multi' | None --> Bool

    Used for development purposes to see if extra processes were being created.
    In autofront's case, __name__ is actually 'autofront.multi' instead of '__main__'.
    No extra processes are created in the present version, but function is still used
    for safety purposes.
    """
    if __name__ == 'autofront.multi':
        return True
    print('Name is {} instead of autofront.multi'.format(__name__))
    return False

def create_process(function, *args, type='script', join=True, timeout=None,
                   **kwargs):
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
    if not test_for_multi(): #Can potentially avoid creating redundant processes
        print('Aborted extra process creation')
        return
    type_dict = {'script':script_worker,
                 'function':function_worker,
                 'input':input_worker}
    target = type_dict[type] #Get correct function for process type
    name = function.__name__
    args = tuple([function] + list(args))
    start_time = time.time()
    worker = multiprocessing.Process(target=target, name=name, args=args, kwargs=kwargs)
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
            kill(worker)
        else:
            print('{} finished normally'.format(worker.name))
        status['waiting'] = False
        
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
    print('Worker {0} alive is {1}'.format(worker.name,
                                           str(worker.is_alive())))
    if worker.is_alive():
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
