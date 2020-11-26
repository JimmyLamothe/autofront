import autofront

def kwarg_printer(**kwargs):
    for kwarg in kwargs:
        print('{0} : {1}'.format(kwarg, kwargs[kwarg]))

autofront.initialize(timeout=3)

autofront.create_route(kwarg_printer)
autofront.create_route(kwarg_printer, live=False, timeout=None, title='kwarg_printer with default kwargs', typed=False)
autofront.create_route(kwarg_printer, live=False, timeout=None, title='kwarg_printer with default kwargs and test kwarg', typed=False, test_kwarg='test_kwarg')

autofront.run()
