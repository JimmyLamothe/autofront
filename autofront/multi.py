#import functools
import multiprocessing
import time
#from utilities import redirect_print
#from input_utilities import redirect_input

worker_dicts = []

config = {'worker_limit':3,
          'timeout':10}

#@functools.wraps
def test_function(*args, **kwargs):
    print('Here are your args: {}'.format(str(args)))
    print('Here are your kwargs: {}'.format(str(kwargs)))
    return 'Task completed'

def test_infinite():
    time.sleep(1000)

def test_join():
    print('Joining in 5 seconds')
    time.sleep(5)
    
def test_worker(function, *args, **kwargs):
    print(function(*args, **kwargs))

#@functools.wraps    
#@redirect_print
def standard_worker(function, *args, **kwargs):
    print(function(*args, **kwargs))

#@functools.wraps
#@redirect_print
#@redirect_input
def input_worker(function, *args, **kwargs):
    print(function(*args, **kwargs))

def get_running_time(worker_dict):
    current_time = time.time()
    start_time = worker_dict['start_time']
    running_time = current_time - start_time
    return running_time

def create_process(function, *args, type='test', join=False, timeout=config['timeout'],
                   **kwargs):
    type_dict = {'test':test_worker,
                 'standard':standard_worker,
                 'input':input_worker}
    target = type_dict[type]
    name = function.__name__
    args = tuple([function] + list(args))
    start_time = time.time()
    timeout = timeout #To be customized
    worker = multiprocessing.Process(target=target, name=name, args=args, kwargs=kwargs)
    worker.start()
    if join:
        print('Waiting for process to finish')
        worker.join()
    else:
        worker_dict = {'worker':worker,
                       'start_time':start_time,
                       'timeout':timeout}
        worker_dicts.append(worker_dict)
    
def is_alive(worker_dict):
    return worker_dict['worker'].is_alive()

def timeout_expired(worker_dict):
    timeout = worker_dict['timeout']
    if timeout:
        return get_running_time(worker_dict) > worker_dict['timeout']
    return False
        

def timeout_okay(worker_dict):
    return not timeout_expired(worker_dict)

def cleanup():
    global worker_dicts
    print('Removing dead processes')
    worker_dicts = list(filter(is_alive, worker_dicts))
    print('Removing processes still running past timeout')
    for worker_dict in filter(timeout_expired, worker_dicts):
        worker_dict['worker'].terminate()
    worker_dicts = list(filter(timeout_okay, worker_dicts))
    limit = config['worker_limit']
    if limit:
        while len(worker_dicts) > limit:
            print('Too many workers, ending oldest process')
            worker_dicts[0]['worker'].terminate()
            worker_dicts.pop(0)

def kill(worker):
    print('Killing {}'.format(worker.name))
    worker.terminate()
    time.sleep(0.5)
    print('Worker {0} alive is {1}'.format(worker.name,
                                           str(worker.is_alive())))
    if worker.is_alive():
        raise RuntimeError('Failed to kill processe')

def kill_all():
    print('Killing all processes')
    for worker_dict in worker_dicts:
        worker = worker_dict['worker']
        kill(worker)

def info():
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
