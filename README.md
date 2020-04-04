# Automatic front end for Python projects

This package lets you automatically run python functions and view their output
from a browser. Simply import this package and your module in a new python file
and specify the functions you want to make accessible. A flask server will automatically
launch, creating a web page which you can access on the local network.
All functions can be executed with one click and all print calls are redirected
to be displayed on the web page.

Typical usage would be to control home automation, Rapsberry Pi DIY projects, etc.
The web page is very basic and is not meant for an end user. The main purpose
is to allow developers to focus on the back end while still having easy access
to a functional front end. Though the code could be modified to make the server
accessible from outside the local network, this is not recommened for safety reasons.
No work has been done to protect it from hacking attempts and by definition it's designed
to run arbitrary Python code on your computer.