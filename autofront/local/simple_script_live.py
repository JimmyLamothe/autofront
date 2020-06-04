import os
import sys
from autofront.utilities import web_input
input = web_input
os.chdir("/Users/jimmy/Programming/Python/autofront/tests")
sys.path.insert(0, "/Users/jimmy/Programming/Python/autofront/tests")
import sys

print('Runtime arguments: ' + str(sys.argv))


