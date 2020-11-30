import autofront

def empty_arg_test(arg1, kwarg1 = None):
    print('arg1 = {}'.format(arg1))
    print('kwarg1 = {}'.format(kwarg1))

autofront.add(empty_arg_test, live=True, join=True)
autofront.add('conditional_input_script.py', live=True)

autofront.run()
