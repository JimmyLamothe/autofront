import os
import sys
from autofront.utilities import web_input
input = web_input
os.chdir("/Users/jimmy/Programming/Python/autofront/tests")
sys.path.insert(0, "/Users/jimmy/Programming/Python/autofront/tests")
import sys
import os
from simple_functions import foo, return_value

print('sys.path: ' + str(sys.path))
print('cwd: ' + os.getcwd())
print('__file__: ' + __file__)
