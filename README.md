# Autofront

Autofront is an automatic front-end for Python developers. In theory, any function or script can be run directly from any web browser on your local network. The function executes as normal and all print calls are displayed in the browser, along with any return value.

A typical use case would be to run something from your phone without needing to design a front-end. Autofront can give you a simple remote control and display for a home automation project, a Spotify player, a Raspberry Pi, whatever you need.

The page design is very basic and functional. If the project proves popular, different basic templates might be developed for specific project types. You can create a custom template to suit your needs, though at that point you might prefer to use Flask directly.

## Installing

On Mac or Linux, use pip:

```
pip install autofront
```

For Windows, follow the usual procedure you use to install packages. This should typically use pip as well.

Autofront uses Flask to run the web server and will install it as a dependency if necessary. Since Autofront is still in alpha, it's recommended to install it in a virtual environment, if this is not already your usual procedure.

This link explains how to [install packages and virtual environments](https://packaging.python.org/tutorials/installing-packages/).

Autofront requires Python 3.

## Usage

Basic usage is simple:

```python
import autofront
from my_module import my_function

autofront.initialize()

autofront.create_route(my_function)

autofront.run()
```

* Create a new file.
* Import Autofront and your functions.
* Initialize the server.
* Create routes to your functions.
* Start the server.

This will start a simple Flask server at 0.0.0.0:5000. Access it from any browser on the same computer. You'll find a simple web page with the name of your function and a "Go" button. Click on the button to run your function. 

This is useful for development and gives you a simple web-based graphical interface for your programs. But you can also easily access the server from your phone or another computer on the local network.

First, you need the local ip address of the computer running the autofront Flask server. This step varies from system to system. On Mac or Linux, try typing the following command in the terminal:

```
ipconfig getifaddr en0
```

Here is the procedure for [Windows 10](https://support.microsoft.com/fr-ca/help/4026518/windows-10-find-your-ip-address)

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