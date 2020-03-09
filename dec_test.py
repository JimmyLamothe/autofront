import contextlib

def redirect_print(func):
    def inner1():
        with open('test', 'w') as out:
            with contextlib.redirect_stdout(out):
                print('inner1')
                return func()
    return inner1

@redirect_print
def test_dec():
    print('test_dec')
    return 'return'

print(test_dec())
