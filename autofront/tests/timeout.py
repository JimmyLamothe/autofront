import time
import autofront

def hanging_function(timeout=autofront.config.config['timeout']):
    time_slept = 0
    print('Timeout is set at {} seconds'.format(str(timeout)))
    while True:
        time.sleep(1)
        time_slept += 1
        print('Sleeping for {} seconds'.format(str(time_slept)))
        if time_slept > timeout:
            print('Warning! Still running past timeout')

autofront.create_route(hanging_function, 5, timeout=5, title='hanging_join_5')

autofront.create_route(hanging_function, join=False, title='hanging_no_join')

autofront.create_route(hanging_function, 5, join=False, timeout=5,
                       title='hanging_no_join_5')

autofront.run()
