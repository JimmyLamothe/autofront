# Autofront

Autofront is an automatic web interface for Python developers. In theory, any function or script can be triggered directly from a web browser on your local network. The function executes as normal and all print calls are displayed in the browser, along with any return value. Any input calls are redirected to the browser for user input.

This lets you control programs from your phone without needing to design an interface. Autofront can become a simple remote control and display for a Raspeberry Pi project, a command center for your programs, a music player, a simple prototype, anything you need.

The goal is to have basically no learning curve. With two imports and two lines of code, you can trigger a function from your phone. Autofront might not be compatible with your code, especially in these early alpha versions, but you'll find out quickly without wasting time. And if it works, you can go right back to programming the back-end.

We also hope it can be used in schools teaching basic Python programming. All student programs can be gathered on one page and run from any student's phone anywhere in the school. The next alpha version should add support for remote access as well so they can do the same outside school.

Autofront's page design is basic and functional. If the project proves popular, different templates might be developed for specific project types. You can also create a custom template to suit your needs, or use custom CSS and Javascript. This requires basic knowledge of web design and Flask. [Read the Flask docs for more information](https://flask.palletsprojects.com/en/1.1.x/#user-s-guide).

If your function or script does not work with autofront, help us out by letting us know. Please make sure that you can correctly run the [test suite](https://github.com/JimmyLamothe/autofront/wiki/Examples-and-tests#test-suit) on your system before [raising an issue](https://github.com/JimmyLamothe/autofront/issues).

## Wiki

Please consult the [Autofront wiki](https://github.com/JimmyLamothe/autofront/wiki/Adding-routes) for more detailed information on adding routes to functions and scripts. This readme only explains the basics.

# Quickstart

## Installing

Use pip:

```
pip install autofront
```

Autofront uses Flask to run the web server and will install it as a dependency if necessary. Since Autofront is still in alpha, it's recommended to install it in a virtual environment, if this is not already your usual procedure. 

This link explains how to [install packages and virtual environments](https://packaging.python.org/tutorials/installing-packages/).

Autofront requires Python 3.6 or higher and was tested on MacOS, Windows 10, Linux and Raspberry Pi. It hasn't been tested yet on Python 3.9 but should work in theory.

## Usage

Basic usage is simple:

```python
import autofront
from my_module import my_function

autofront.add(my_function)

autofront.run()
```
* Create a new Python script.
* Import autofront and your functions.
* Add routes to your functions.
* Start the server.

A Flask server will launch at ```0.0.0.0:5000``` (or ```localhost:5000```). Access it from any browser on the same computer. You'll find a page with the name of your function and a "Go" button. Click it to trigger your function.

This is useful for development and gives you a simple web-based interface for your programs. But you can also easily access the server from your phone or another computer on the local network. When you start the server, autofront prints your local IP address to the console. Simply type the address in your browser (for example: ```192.168.0.179:5000```). Local IP addresses rarely change on your local network, so you can bookmark it for future use. If it does change, simply look it up in the console the next time you start your server.

If autofront fails to detect your local IP, you can easily google the correct method to find it on your operating system. Just google ```get local ip address [name_of_your_os]```.

You can now trigger your functions and scripts from any browser connected to your local network.

See [Adding routes](https://github.com/JimmyLamothe/autofront/wiki/Adding-routes) for more detailed information on adding routes to functions and scripts.

## Contributing

Autofront is open to outside contributors. As it's currently in alpha, the process is still to be determined. 

## Credits

Autofront was designed by Jean-Michel Laprise.