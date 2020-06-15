""" Test module for autofront package

This module starts a Flask server and tests route detection.

"""
import autofront
from simple_functions import detect_function

autofront.initialize()

autofront.create_route(detect_function)

autofront.create_route('detect_script.py')

#autofront.create_route(8) #Uncomment to test exception message

autofront.run()

