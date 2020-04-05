import sys, subprocess
from flask import Flask, redirect, url_for, render_template
from autofront.decorators import redirect_print


print('Development version active')

app = Flask(__name__)

def clear_display():
    with open('autofront/display.txt', 'w') as out:
        pass

clear_display()

func_dicts = [] #List of link address and link name for each function

#TO DO: Make multiple page formats - (choose layout, change title, etc)
def functions():    
    with open('autofront/display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return render_template('functions.html', title = 'functions', display = display,
                           func_dicts = func_dicts)

app.add_url_rule('/', 'functions', functions)

def run_script(script, *args):
    def new_function():
        with open('autofron/display.txt', 'a') as out:
            subprocess.run(script, *args, stdout = out)
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

    func_dicts.append({'link':link, 'title':title})

def run(host='0.0.0.0', port = 5000):
    app.run(host = host, port = port)
