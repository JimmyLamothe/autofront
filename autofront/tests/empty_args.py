import autofront

def empty_arg_test(arg1, kwarg1 = None):
    print('arg1 = {}'.format(arg1))
    print('kwarg1 = {}'.format(kwarg1))

autofront.create_route(empty_arg_test, live=True, join=True)
autofront.create_route('conditional_input_script.py', live=True)

autofront.run()
