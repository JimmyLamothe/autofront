""" Test module for autofront package

This module starts a Flask server and tests route detection.

"""
import autofront
from simple_functions import detect_function

autofront.initialize()

autofront.add(detect_function)

autofront.add('detect_script.py')

#autofront.add(8) #Uncomment to test exception message

autofront.run()

