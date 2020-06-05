import sys
import os
from simple_functions import foo, return_value

print('sys.path: ' + str(sys.path))
print('cwd: ' + os.getcwd())
print('__file__: ' + __file__)
