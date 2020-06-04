import os
import sys
from autofront.utilities import web_input
input = web_input
os.chdir("/Users/jimmy/Programming/Python/autofront/tests")
sys.path.insert(0, "/Users/jimmy/Programming/Python/autofront/tests")
import sys

args = sys.argv

print('It works!')

if len(args) == 1:
    print('But you forgot the args.')
    sys.exit(0)

else:
    args = args[1:]

print('Here are your args:')

for arg in args:
    print(arg)
