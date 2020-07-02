import multiprocessing
import time
from autofront.config import config
from autofront.input_utilities import redirect_input
from autofront.utilities import redirect_print

worker_dicts = []
    
def script_worker(function, *args, **kwargs):
    function(*args, **kwargs)

@redirect_print
def function_worker(function, *args, **kwargs):
    return_value = function(*args, **kwargs)
    if return_value:
        print(return_value)

@redirect_print
@redirect_input
def input_worker(function, *args, **kwargs):
    return_value = function(*args, **kwargs)
    if return_value:
        print(return_value)

def get_running_time(worker_dict):
    current_time = time.time()
    start_time = worker_dict['start_time']
    running_time = current_time - start_time
    return running_time

def test_for_main():
    if __name__ == '__main__':
        return True
    else:
        print('name is {} instead of __main__'.format(__name__))

def create_process(function, *args, type='script', join=False, timeout=config['timeout'],
                   **kwargs):
    if not test_for_main(): #Doing it this way to avoid indenting rest of function
        pass
    type_dict = {'script':script_worker,
                 'function':function_worker,
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
