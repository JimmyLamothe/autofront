""" This test is used to make sur only the kwargs for the function make it
into the triggered function, not those meant for autofront.
"""
import autofront

def kwarg_printer(**kwargs):
    for kwarg in kwargs:
        print('{0} : {1}'.format(kwarg, kwargs[kwarg]))

autofront.initialize(timeout=3)

autofront.add(kwarg_printer)
autofront.add(kwarg_printer, live=False, timeout=None,
              title='kwarg_printer with default kwargs', typed=False)
autofront.add(kwarg_printer, live=False, timeout=None,
              title='kwarg_printer with default kwargs and test kwarg',
              typed=False, test_kwarg='test_kwarg')

autofront.run()
