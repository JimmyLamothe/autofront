This directory contains different tests used while developping autofront.

You can use them to troubleshoot your own autofront scripts.

autotest.py contains the main tests for different kinds of routes.
If you're having trouble getting one of your functions to work, consult
the equivalent code in autotest.py to make sure you're using the correct syntax
for the kind of route you're trying to make.

If you're getting unexpected errors, run 'autotest.py' to make sure
that autofront is functioning correctly on your system. The autofront wiki
at https://github.com/JimmyLamothe/autofront/wiki gives required inputs
and expected outputs for each test route.

Other tests used in development:

autoled.py - Raspberry Pi GPIO calls

detect_test.py - Script and function detection

duplicate_title.py - Duplicate titles should raise an exception

static_test.py - Loads custom CSS from static directory

template_test.py - Loads custom HTML from templates directory

timeout.py - Function and script timeout behavior


Other files in test directory are used by these test scripts.
