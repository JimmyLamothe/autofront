import time

def test_function(*args, **kwargs):
    print('Here are your args: {}'.format(str(args)))
    print('Here are your kwargs: {}'.format(str(kwargs)))
    return 'Task completed'

def test_infinite():
    time.sleep(1000)

def test_join():
    print('Joining in 5 seconds')
    time.sleep(5)
