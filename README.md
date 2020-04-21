# Autofront

Autofront is an automatic front-end for Python developers. In theory, any function or script can be run directly from any web browser on your local network. The function executes as normal and all print calls are displayed in the browser, along with any return value.

The most typical use case would be to run stuff from your phone without needing to design a front-end. It can be a remote control and display for a home automation project, a Spotipy player, a Raspberry Pi, whatever you need.

The page design is extremely basic and functional. If the project proves popular, different basic templates might be developed to suit different use cases. You can create a custom template to suit your needs, though at that point it's probably just as simple to use Flask directly.

## Installing

Installing Autofront is simple. On Mac or Linux, simply use pip:

```
pip install autofront
```

For Windows, follow the usual procedure you use to install packages. This should typically use pip as well.

Autofront uses Flask to run the web server and will install it as a dependency if necessary. Since Autofront is still in alpha, it's recommended to install it in a virtual environment, if this is not already your usual procedure.

The following link explains how to install packages and run virtual environments in detail:

https://packaging.python.org/tutorials/installing-packages/

Autofront requires Python 3.

## Usage

Basic usage is very simple:

```python
import autofront
from my_module import my_function

autofront.create_route(my_function)

autofront.run()
```

This will start a simple Flask server at localhost:5000. You can access it from any browser. You'll find a simple web page with your function as a link. Click on the link to run your function. 

Accessing the function on localhost:5000 is great for development and gives you a simple web-based graphical interface for your programs. But you can also easily access the front-end from your phone or a browser on another computer.

First, you need to find the local ip address of the computer running the autofront Flask server. This step varies from system to system. On Mac or Linux, try typing the following command in the terminal:

```
ipconfig getifaddr en0
```

For Windows 10, the following link explains the procedure:

https://support.microsoft.com/fr-ca/help/4026518/windows-10-find-your-ip-address

Enter the correct address and the port in your web browser in the following format:

```
ipaddress:port
```

For example:

```
192.168.0.179:5000
```

You can now run your functions and scripts from any browser connected to your local network.

Please consult the [Autofront wiki](https://github.com/JimmyLamothe/autofront/wiki/Creating-routes) for more detailed information on creating routes to functions and scripts.

## Contributing

Autofront is open to outside contributors. As it's currently in alpha, the process is still very much to be determined.

## Credits

Autofront was designed by Jean-Michel Laprise.
