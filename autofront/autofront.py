""" Main module for autofront, the automatic front-end

This module lets users create routes to other functions and scripts
they've written. It starts a simple Flask server with one page from which
you can execute functions and see the result of their print calls
and their return values as strings. It also replaces regular input calls
with a version that gets user input in the browser.


Here is the basic usage::

    import autofront
    from my_module import my_function

    autofront.create_route(my_function)

    autofront.run()

That's all the code needed for a simple function with no arguments.

To create a route to a script::

    autofront.create_route('my_script.py')

To create a route with fixed arguments::

    autofront.create_route(my_function, 'arg1', 'arg2', kwarg1='bar')

To create a route with args input in browser at runtime::

    autofront.create_route(my_function, live=True)

To create a route with live args using type indications::

    autofront.create_route(my_function, live=True, typed=True)

To create a second route to the same function or script::
    autofront.create_route(my_function, title = new_name, link = new_name)

To create a route to a function or script meant to run in the background::
    autofront.create_route(my_function, join=False)

Scripts should be detected automatically. If detection fails, you can specify
the script kwarg::
    autofront.create_route('my_script.py', script=True)

Functions and scripts with input calls should be detected automatically. If detection
fails, you can specify the input_call kwarg::
    autofront.create_route(my_function, input_call=True)

You can configure certain options with autofront.initialize (see function docstring).
This must be done before creating any routes, otherwise the server will be initialized
automatically using default options.

"""
import multiprocessing
import os
import pprint
from flask import Flask, redirect, render_template, request, url_for  
from autofront.config import config, status
from autofront.detect import detect_input, detect_script, key_in_kwargs
from autofront.input_utilities import clear_input, clear_prompt, get_input
from autofront.input_utilities import get_input_args, get_input_kwargs, get_prompt
from autofront.input_utilities import get_timeout, initialize_prompt, put_input_args
from autofront.input_utilities import redirect_input, wait_for_prompt, write_input
from autofront.multi import cleanup_workers, create_process, status
from autofront.utilities import add_args_to_title, cleanup, clear_display
from autofront.utilities import create_local_script, get_display, get_fixed_args
from autofront.utilities import get_function, get_live_args, get_script_path
from autofront.utilities import is_live, is_script, needs_input, print_return_value
from autofront.utilities import print_route_dicts, redirect_print, title_exists
from autofront.utilities import typed_args, wait_to_join, wrap_script

app = None # This will be a Flask server created by initialize().

def functions():
    """ Main page displaying all functions and their print calls """
    #print_route_dicts() #Uncomment to check route dicts
    cleanup_workers() #Terminate any dead or potentially hanged processes
    if request.method == 'POST':
        status['request_received'] = True
        status['request_completed'] = False
        title = list(request.form.keys())[0] #Corresponds to 'input name' in HTML
        join = wait_to_join(title)
        timeout = get_timeout(title)
        if is_script(title): #Path for scripts
            script_path = get_script_path(title)
            args = get_fixed_args(title)[0]
            if is_live(title): #For scripts with args input in browser
                args += get_live_args(request)[0]
            if needs_input(title): #For scripts with input calls
                print('Input script detected')
                initialize_prompt()
                put_input_args(title, args) 
                return redirect(url_for('browser_input', title=title))
            else:
                script = create_local_script(script_path)
                wrapped_script = wrap_script(script, *args)
                print('Creating process for {}'.format(title))
                create_process(wrapped_script, type='script', join=join,
                               timeout=timeout)
                return redirect(url_for('functions'))
        function = get_function(title) #Path for function calls
        fixed_args = get_fixed_args(title)
        args = fixed_args[0]
        kwargs = fixed_args[1]
        if is_live(title): #For functions with args input in browser
            typed = typed_args(title)
            live_args = get_live_args(request, typed=typed)
            args += live_args[0]
            kwargs.update(live_args[1])
        if needs_input(title): #For functions that use input calls
            print('Input function detected')
            initialize_prompt()
            put_input_args(title, args, kwargs=kwargs)
            return redirect(url_for('browser_input', title=title))
        print('Creating process for {}'.format(title))
        create_process(function, *args, type='function', join=join,
                       timeout=timeout, **kwargs)
    display = get_display()
    clear_display()
    route_dicts = config['route_dicts']
    top = config['top']
    return render_template('functions.html', title='functions', top=top,
                           display=display, route_dicts=route_dicts)

def browser_input(title):
    """ Page to get input from user - run multiple times per script or function

    Step 1: First run when input script or function has been detected.
            Starts script or function.
    Step 2: Run as many times as there are input calls - displays prompt
            and gets input
    Step 3: Run as many times as there are input calls - sends user input
            to script or function and waits until it exits or timeouts
            or there is another input call.

    """
    display = get_display()
    #Step 3 - Script or function running - Input received
    if request.method == 'POST':
        clear_display()
        form_data = request.form
        input_data = form_data['Input']
        write_input(input_data)
        wait_for_prompt(timeout=get_timeout(title))
        return redirect(url_for('browser_input', title=title))
    prompt = get_prompt()
    #STEP 1 - Script or function not running - Launch it, get first prompt
    if prompt == 'waiting for prompt':
        clear_prompt()
        clear_input()
        timeout = get_timeout(title)
        if is_script(title): #Script path
            script_path = get_script_path(title)
            args = get_input_args(title)
            script = create_local_script(script_path)
            wrapped_script = wrap_script(script, *args)
            print('creating process for {}'.format(title))
            create_process(wrapped_script, type='script', join=False,
                           timeout=timeout)
            wait_for_prompt()
            return redirect(url_for('browser_input', title=title))
        else: #Function path
            function = get_function(title)
            args = get_input_args(title)
            kwargs = get_input_kwargs(title)
            print('creating process for {}'.format(title))
            create_process(function, *args, type='input', join=False,
                           timeout=timeout, **kwargs)
            wait_for_prompt()
            return redirect(url_for('browser_input', title=title))
    elif prompt == 'finished' or prompt == 'timeout reached':
        return redirect(url_for('functions'))
    #STEP 2 - Script or function running - get input in browser
    if prompt == 'None':
        prompt = ''
    return render_template('web_input.html', title= 'get_input',
                           display=display, prompt=prompt)

def initialize(name=__name__, print_exceptions=True, template_folder=None,
               static_folder=None, timeout=10, top=False, worker_limit=20):
    """ Initialize the Flask app and clear the display. Running this after
    a route is created will delete all routes from memory.

    The print_exceptions kwarg lets you enable or disable printing
    runtime exceptions to the browser.

    Set top to True to display print calls and return calls at the top
    of the screen on the default template instead of at the bottom.

    The template_folder option lets you specify the filepath to a folder
    containing a custom 'functions.html' template.

    The static folder option lets you specify the filepath to a folder
    containing a custom 'main.css' file. This folder must be named 'static'
    and must contain a folder called 'css'. The 'main.css' file must be in
    this 'css' folder. The actual folder to point to in the kwarg
    is the one called 'static'.

    The timeout and worker_limit kwargs let you deal with functions or scripts
    that hang and slow down your program. The maximum number of functions or
    scripts that can run in the background at the same time is defined by worker_limit.
    The maximum amount of time a function or script can run is defined by timeout.
    Lowering these values can help speed up functionality in case a function or script
    doesn't finish properly.

    """
    cleanup()
    config['top'] = top
    config['print_exceptions'] = print_exceptions
    config['timeout'] = timeout
    config['worker_limit'] = worker_limit
    clear_display()
    global app
    if template_folder and static_folder:
        app = Flask(name, template_folder=template_folder,
                    static_url_path=static_folder)
    elif template_folder:
        app = Flask(name, template_folder=template_folder)
    elif static_folder:
        app = Flask(name, static_folder=static_folder)
    else:
        app = Flask(name)
    app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])
    app.add_url_rule('/browser_input/<title>', 'browser_input',
                     browser_input, methods=['GET', 'POST'])

def initialize_default():
    """ Initializes the flask server with deault settings """
    print('Initializing server with default settings.')
    print('Run autofront.initialize() before creating routes to ' +
          'set optional settings.')
    initialize()
    
def create_route(function_or_script_path, *args, input_call=False,  join=True,
                 live=False, script=False, timeout=None, title=None, typed=False,
                 **kwargs):
    """ Create a new route to a function or script

    If you need to specify initialization values, this must be done before
    creating the first route.

    Usage is explained in docs and main module doc string.

    Specify a title in the kwargs if you want a custom string displayed
    in the browser instead of your function name or script filename.

    Each function or script must have a different title.

    Use live=True to input args at runtime (can be combined with fixed args).

    Use join=False for functions or scripts meant to run in the background.
    This is automatic for functions with input calls.

    Use typed=True to use type indications in your live args.

    Use script=True if detection fails to identify a script

    Use input_call=True if detection fails to identify that there are input calls

    Specify a timeout value (timeout=...) if a script of function hangs
    and needs to be stopped automatically.

    """
    if not app:
        initialize_default()
    if not key_in_kwargs('script', **kwargs):
        script = detect_script(function_or_script_path)
    if script:
        script_path = function_or_script_path
        function = None
        name = script_path
        if not key_in_kwargs('input_call', **kwargs):
            input_call = detect_input(script_path, script=True)
    else:
        function = function_or_script_path
        script_path = None
        name = function.__name__
        if not key_in_kwargs('input_call', **kwargs):
            input_call = detect_input(function)
    if not title:
        title = name
    if title_exists(title):
        message = 'A route with this title already exists.\n'
        message += 'Please specify a new title with the title kwarg.\n'
        message += "Example: create_route(my_function, title='new_title')\n"
        raise ValueError(message)
    link = title
    if not timeout:
        if join:
            timeout = config['timeout']
        else:
            timeout = None #These functions need to keep running in background
    app.add_url_rule('/' + link, link)
    config['route_dicts'].append({'function':function, #None if script
                                  'script':script, #True if script, False if function
                                  'script_path':script_path, #None if function
                                  'args':[*args],
                                  'kwargs':{**kwargs},
                                  'typed':typed,
                                  'link':link,
                                  'title':title,
                                  'live':live,
                                  'input_call':input_call,
                                  'join':join,
                                  'timeout':timeout})
    if live:
        config['route_dicts'][-1]['title'] = add_args_to_title(title, [*args],
                                                    script=script)

def run(host='0.0.0.0', port=5000):
    """ Starts the Flask server """
    if not app:
        raise RuntimeError('Routes must be created before starting server.')
    app.run(host=host, port=port)
