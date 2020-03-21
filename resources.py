#Resources needed in different files

import tempfile, atexit

def initialize_display():
    return tempfile.TemporaryFile(mode='a+t')

display = initialize_display()

@atexit.register
def close_display():
    print('Deleting Temp Files')
    display.close()
    print('Temp Files Deleted')
