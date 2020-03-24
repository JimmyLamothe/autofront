import sys
from flask import Flask, redirect, url_for, render_template
from decorators import redirect_print

app = Flask(__name__)

def clear_display():
    with open('display.txt', 'w') as out:
        pass

clear_display()

func_dicts = []

def functions():    
    with open('display.txt', 'r') as filepath:
        display = filepath.read()
        display = display.split('\n')
    return render_template('functions.html', title = 'functions', display = display,
                           func_dicts = func_dicts)

app.add_url_rule('/', 'functions', functions)

def create_route(function, link = None, title = None):
    if not link:
        link = function.__name__
    if not title:
        title = function.__name__
    def new_route():
        clear_display()
        @redirect_print
        def new_route():
            function()
        new_route.__name__ = function.__name__
        new_route()
        return redirect(url_for('functions'))

    app.add_url_rule('/' + link, link, new_route)

    func_dicts.append({'link':link, 'title':title})
