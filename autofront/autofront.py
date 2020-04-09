import sys, subprocess
from flask import Flask, redirect, url_for, render_template, request
from autofront.decorators import redirect_print, display_path
from autofront.utilities import parse_args, get_function

print('Development version active')

app = Flask(__name__)

def clear_display():
    with open(display_path + '/display.txt', 'w') as out:
        pass

clear_display()

func_dicts = [] #List of link address and link name for each function


#TO DO: Make multiple page formats - (choose layout, change title, etc)
def functions():
    if request.method =='POST':
        func_name = list(request.form.keys())[0]
        function = get_function(func_name, func_dicts)
        arg_string = list(request.form.values())[0]
        all_args = parse_args(arg_string)
        args = all_args[0]
        kwargs = all_args[1]
        clear_display()
        @redirect_print
        def new_function():
            function(*args, **kwargs)
        new_function.__name__ = function.__name__
        new_function()
        return redirect(url_for('functions'))
    with open(display_path + '/display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return render_template('functions.html', title = 'functions', display = display,
                           func_dicts = func_dicts)

app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])

def run_script(script, *args):
    script_path = './' + script
    command_list = list(args)
    command_list.insert(0, script_path)
    command_list.insert(0, 'python')
    print(command_list)
    def new_function():
        with open(display_path + '/display.txt', 'a') as out:
            subprocess.run(command_list, stdout = out)
    new_function.__name__ = script
    return new_function

def create_route(function, *args, link = None, title = None, **kwargs):
    if not link:
        link = function.__name__
    if not title:
        title = function.__name__
    def new_route():
        clear_display()
        @redirect_print
        def new_route():
            function(*args, **kwargs)
        new_route.__name__ = function.__name__
        new_route()
        return redirect(url_for('functions'))
    app.add_url_rule('/' + link, link, new_route)
    func_dicts.append({'func': function, 'link':link,
                       'title':title, 'live':False})

def create_live_route(function, *args, link = None, title = None, **kwargs):
    create_route(function, *args, link = link, title = title, **kwargs)
    func_dicts[-1]['live'] = True

def run(host='0.0.0.0', port = 5000):
    app.run(host = host, port = port)
