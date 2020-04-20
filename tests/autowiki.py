""" Examples for the autofront wiki

This module starts a Flask server with a route to the example number
specified in the command line args. The purpose is to test the wiki
and to generate updated screen shots when the code or template changes.

Usage : python autowiki 1 --> loads the routes for the first example

"""
import sys

args = sys.argv

if len(args) > 2:
    if args[2] == 'dev': #This is only used for development. 
        sys.path.insert(1, '/Users/jimmy/Programming/Python/autofront/')
        args.pop(2)
    else:
        sys.exit('Invalid arguments')

import autofront
    
page = args[1]

from wiki_functions import my_function

page_dict = {'1' : [my_function]}

for function in page_dict[page]:
    autofront.create_route(function)

autofront.run()

