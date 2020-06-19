""" Main module for autofront automatic front-end

This module lets users create routes to other functions and scripts
they've written. It starts a simple Flask server with one page from
where you can execute functions, see the result of their print calls
and see their return values in string form.

Here is the basic usage::

    import autofront
    from my_module import my_function

    autofront.initialize()

    autofront.create_route(my_function)

    autofront.run()


That is all the code needed for a simple function with no arguments.


To create a route with fixed arguments::

    autofront.create_route(my_function, 'foo', kwarg1='bar')

To create a route with args input in browser at runtime::

    autofront.create_route(my_function, live=True)

To create a route with live args using type indications::

    autofront.create_route(my_function, live=True, typed=True)

To create a route to a script::

autofront.create_route('my_script.py', script = True)

To create a route to a script with arguments::

    autofront.create_route('my_script.py', 'foo', script = True)

To create a route to a script with args input in browser at runtime::

    autofront.create_route(my_script.py, script = True, live = True)

To create a second route to the same function or script::
    autofront.create_route(my_function, title = new_name, link = new_name)

To create a special route allowing runtime exceptions
to be caught and displayed in the broswer::

    autofront.create_route(autofront.utilities.raise_exceptions)


"""
import os
import atexit
import threading
from flask import Flask, redirect, url_for, render_template, request
from autofront.utilities import redirect_print, clear_display, get_display
from autofront.utilities import run_script, add_args_to_title, input_script
from autofront.utilities import get_function, get_live_args, get_fixed_args
from autofront.utilities import is_script, is_live, typed_args, print_return_value
from autofront.utilities import browser_exceptions, create_local_script
from autofront.utilities import clear_local_files, get_script_path
from autofront.input import initialize_prompt, initialize_input
from autofront.input import get_prompt, get_input, wait_for_prompt
from autofront.input import put_input_args, get_input_args, write_input
from autofront.input import clear_prompt, clear_input
from autofront.input import start_process
from autofront.detect import detect_script, detect_input, key_in_kwargs

app = None # This will be a Flask server created by initialize().

func_dicts = [] # All function dicts generated by create_route().

config = {'timeout':5}

#@redirect_print
def functions():
    """ Landing page displaying all functions and their print calls """
    if request.method == 'POST':
        func_title = list(request.form.keys())[0] #From HTML: input name=...
        if is_script(func_title, func_dicts):
            clear_display()
            script_path = get_script_path(func_title, func_dicts)
            args = get_fixed_args(func_title, func_dicts)[0]
            if is_live(func_title, func_dicts):
                args += get_live_args(request)[0]
            if detect_input(script_path):
                print('input script detected')
                initialize_prompt()
                put_input_args(func_title, func_dicts, args)
                return redirect(url_for('browser_input', title=func_title))
            else:
                script = create_local_script(script_path)
                run_script(script, *args)()
                return redirect(url_for('functions'))
        function = get_function(func_title, func_dicts)    
        fixed_args = get_fixed_args(func_title, func_dicts)
        args = fixed_args[0]
        kwargs = fixed_args[1]
        if is_live(func_title, func_dicts):
            typed = typed_args(func_title, func_dicts)
            live_args = get_live_args(request, typed=typed)
            args += live_args[0]
            kwargs.update(live_args[1])
        clear_display()
        @redirect_print
        def wrapper():
            return function(*args, **kwargs)
        wrapper.__name__ = function.__name__
        return_value = wrapper()
        if return_value:
            print_return_value(return_value)
        return redirect(url_for('functions'))
    display = get_display()
    return render_template('functions.html', title='functions',
                           display=display, func_dicts=func_dicts)

#Stores the processes for the currently running input function or script
processes = {'input':None, 'view':None}

def browser_input(title):
    """ Page to get input from user - run multiple times per scripts

    Step 1: First run when input script has been detected - starts script
    Step 2: Run as many times as there are input calls - displays prompt
            and gets input
    Step 3: Run as many times as there are input calls - sends user input
            to script and waits until script is finished or there is
            another input call. If script is meant to keep running,
            kwarg 'timeout=secs' sets a number of seconds after which
            to load the main page. By default, this is set at 10 seconds.
            If this is set too low, script might not have time to finish
            before it is aborted.

    """
    display = get_display()
    print('DISPLAY' + str(display))
    #Step 3 - Script running - Input received
    if request.method == 'POST':
        clear_display()
        form_data = request.form
        input_data = form_data['Input']
        write_input(input_data)
        print(get_input())
        wait_for_prompt(timeout=config['timeout'])
        return redirect(url_for('browser_input', title=title))
    print('getting input')
    prompt = get_prompt()
    print('prompt == ' + prompt)
    #STEP 1 - Script not running - Starting script, getting first prompt
    if prompt == 'waiting for prompt':
        clear_prompt()
        clear_input()
        script_path = get_script_path(title, func_dicts)
        args = get_input_args(title, func_dicts)
        script = create_local_script(script_path)
        thread_script = run_script(script, *args)
        processes['input'] = threading.Thread(target=thread_script)
        processes['input'].start()
        wait_for_prompt()
        return redirect(url_for('browser_input', title=title))
    elif prompt == 'script finished' or prompt == 'timeout reached':
        print('redirecting')
        display = get_display()
        return redirect(url_for('functions'))
    #STEP 2 - Script running - getting input in browser
    if prompt == 'None':
        prompt = ''
    return render_template('web_input.html', title= 'get_input',
                           display=display, prompt=prompt)
"""
    prompt = wait_for_prompt()
    if prompt == 'None':
        prompt = ''
    return render_template('web_input.html', title= 'get_input',
                           display=display, prompt=prompt)
"""

def initialize(name=__name__, raise_exceptions=False, template_folder=None):
    """ Initializes the Flask app and clears the display

    The raise_exceptions kwarg lets you enable or disable printing
    runtime exceptions to the browser versus raising them as usual.

    The template_folder option lets you specify the filepath to a folder
    containing a custom 'functions.html' template.
    """
    cleanup()
    if raise_exceptions:
        browser_exceptions()
    clear_display()
    global app
    if template_folder:
        app = Flask(name, template_folder=template_folder)
    else:
        app = Flask(name)
    app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])
    app.add_url_rule('/browser_input/<title>', 'browser_input',
                     browser_input, methods=['GET', 'POST'])
    
def create_route(function_or_script_path, *args, title=None, link=None, live=False,
                 script=False, input=False, typed=False, **kwargs):
    """ Function to create a new route to a function or script

    Usage is explained in docs and main module doc string.

    Use live=True for args input at runtime.

    Use script=True and the script path as the function positional arg
    to run a script instead of a function.

    Use user_input=True if you get user input using the built-in input function.

    Use typed=True to use type indications in your live args.

    Specify the title kwarg to display a specific string for your
    function in the browser.

    initialize() must be run before creating routes.

    """
    if not key_in_kwargs('script', **kwargs):
        script = detect_script(function_or_script_path)
    if script:
        script_path = function_or_script_path #if script, this is the filepath
        function = None
        name = script_path
    else:
        function = function_or_script_path
        script_path = None
        name = function.__name__
    print('args for ' + name + ': ' + str(args))
    print('kwargs for ' + name + ': ' + str(kwargs))
    if not link:
        link = name
    if not title:
        title = name
    if not app:
        raise RuntimeError('Initialize app with autofront.initialize() '+
                           'before you create routes.')
    app.add_url_rule('/' + link, link)
    func_dicts.append({'function':function,
                       'script_path':script_path,
                       'args':[*args],
                       'kwargs':{**kwargs},
                       'link':link,
                       'title':title,
                       'live':live,
                       'script':script,
                       'typed':typed})
    if live:
        func_dicts[-1]['title'] = add_args_to_title(title, [*args],
                                                    script=script)

def run(host='0.0.0.0', port=5000):
    """ Starts the Flask server """
    if not app:
        raise RuntimeError('Initialize app with autofront.initialize() '+
                           'before you run it.')
    app.run(host=host, port=port)

def cleanup():
    clear_local_files()
