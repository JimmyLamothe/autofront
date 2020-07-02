""" Main module for Autofront automatAic front-end

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
import multiprocessing
import os
import pprint
from flask import Flask, redirect, render_template, request, url_for  
from autofront.config import config
from autofront.detect import detect_input, detect_script, key_in_kwargs
from autofront.input_utilities import clear_input, clear_prompt, get_input
from autofront.input_utilities import  get_input_kwargs, get_input_args, get_prompt
from autofront.input_utilities import get_timeout, initialize_prompt, put_input_args
from autofront.input_utilities import redirect_input, wait_for_prompt, write_input
from autofront.multi import create_process
from autofront.utilities import add_args_to_title, cleanup, clear_display
from autofront.utilities import create_local_script, get_display, get_fixed_args
from autofront.utilities import get_function, get_live_args, get_script_path
from autofront.utilities import is_live, is_script, is_special, needs_input
from autofront.utilities import print_return_value, print_route_dicts, redirect_print
from autofront.utilities import typed_args, wait_to_join, wrap_script

app = None # This will be a Flask server created by initialize().

def functions():
    """ Main page displaying all functions and their print calls """
    #print_route_dicts() #Uncomment to check route dicts are correct
    if request.method == 'POST': #STEP 2 - Function or script requested from browser
        clear_display()
        title = list(request.form.keys())[0] #Corresponds to 'input name' in HTML
        join = wait_to_join(title)
        timeout = get_timeout(title)
        if is_script(title): #Path for scripts
            script_path = get_script_path(title)
            args = get_fixed_args(title)[0]
            if is_live(title): #For scripts with args input in browser
                args += get_live_args(request)[0]
            if needs_input(title): #For scripts with input calls
                print('input script detected')
                initialize_prompt()
                put_input_args(title, args) 
                return redirect(url_for('browser_input', title=title))
            else:
                script = create_local_script(script_path)
                wrapped_script = wrap_script(script, *args)
                print('creating process for {}'.format(title))
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
            print('input function detected')
            initialize_prompt()
            put_input_args(title, args, kwargs=kwargs)
            return redirect(url_for('browser_input', title=title))
        print('creating process for {}'.format(title))
        create_process(function, *args, type='function', join=join,
                       timeout=timeout, **kwargs)
    display = get_display()
    return render_template('functions.html', title='functions',
                           display=display, route_dicts=config['route_dicts'])

#Stores the process for the currently running input function or script
processes = {'process':None, 'return_value':None}

def browser_input(title):
    """ Page to get input from user - run multiple times per script or function

    Step 1: First run when input script or function has been detected.
            Starts script or function.
    Step 2: Run as many times as there are input calls - displays prompt
            and gets input
    Step 3: Run as many times as there are input calls - sends user input
            to script or function and waits until it exits or there is
            another input call. If script or function is meant to keep running,
            kwarg 'timeout=secs' sets a number of seconds after which
            to load the main page. By default, this is set at 10 seconds.
            If this is set too low, script or function might not have time
            to finish before it is aborted.

    """
    display = get_display()
    print('DISPLAY' + str(display))
    #Step 3 - Script or function running - Input received
    if request.method == 'POST':
        clear_display()
        form_data = request.form
        input_data = form_data['Input']
        write_input(input_data)
        print(get_input())
        wait_for_prompt(timeout=get_timeout(title))
        return redirect(url_for('browser_input', title=title))
    print('getting input')
    prompt = get_prompt()
    print('prompt == ' + prompt)
    #STEP 1 - Script or function not running - Launch it, get first prompt
    if prompt == 'waiting for prompt':
        clear_prompt()
        clear_input()
        join = wait_to_join(title)
        timeout = get_timeout(title)
        if is_script(title):
            script_path = get_script_path(title)
            args = get_input_args(title)
            script = create_local_script(script_path)
            """
            mp_script = wrap_script(script, *args)
            processes['process'] = multiprocessing.Process(target=mp_script)
            processes['process'].start()
            """
            wrapped_script = wrap_script(script, *args)
            print('creating process for {}'.format(title))
            create_process(wrapped_script, type='script', join=False,
                           timeout=timeout)
            wait_for_prompt()
            return redirect(url_for('browser_input', title=title))
        else:
            function = get_function(title)
            args = get_input_args(title)
            kwargs = get_input_kwargs(title)

            print('creating process for {}'.format(title))
            create_process(function, *args, type='input', join=False,
                           timeout=timeout, **kwargs)
            wait_for_prompt()
            return redirect(url_for('browser_input', title=title))
    elif prompt == 'finished' or prompt == 'timeout reached':
        print('redirecting')
        return redirect(url_for('functions'))
    #STEP 2 - Script or function running - get input in browser
    if prompt == 'None':
        prompt = ''
    return render_template('web_input.html', title= 'get_input',
                           display=display, prompt=prompt)

def initialize(name=__name__, raise_exceptions=False, template_folder=None,
               timeout=5, worker_limit=20):
    """ Initializes the Flask app and clears the display

    The raise_exceptions kwarg lets you enable or disable printing
    runtime exceptions to the browser versus raising them as usual.

    The template_folder option lets you specify the filepath to a folder
    containing a custom 'functions.html' template.
    """
    cleanup()
    if raise_exceptions:
        config['print_exceptions'] = False
    else:
        config['print_exceptions'] = True
    config['timeout'] = timeout
    config['worker_limit'] = worker_limit
    clear_display()
    global app
    if template_folder:
        app = Flask(name, template_folder=template_folder)
    else:
        app = Flask(name)
    app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])
    app.add_url_rule('/browser_input/<title>', 'browser_input',
                     browser_input, methods=['GET', 'POST'])

def initialize_default():
    print('Initializing server with default settings.')
    print('Run initialize() before creating routes to' +
          ' set optional settings')
    initialize()
    
def create_route(function_or_script_path, *args, input_call=False,  join=True,
                 link=None, live=False, script=False, timeout=None, title=None, 
                 typed=False, **kwargs):
    """ Function to create a new route to a function or script

    Usage is explained in docs and main module doc string.

    Specify a title in the kwargs if you want a custom string displayed
    in the browser instead of your function name or script filename.

    Use live=True to input args at runtime (can be combined with fixed args).

    Use join=False for functions or script meant to run in the background

    Use typed=True to use type indications in your live args.

    Use script=True if detection fails to identify a script

    Use input_call=True if detection fails to identify that there are input calls

    """
    if not app:
        initialize_default()
    if not key_in_kwargs('script', **kwargs):
        script = detect_script(function_or_script_path)
    if script:
        script_path = function_or_script_path #if script, this is the filepath
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
    print('args for ' + name + ': ' + str(args))
    print('kwargs for ' + name + ': ' + str(kwargs))
    if not link:
        link = name
    if not title:
        title = name
    if not timeout:
        timeout = config['timeout']
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
    print(config['route_dicts'][-1])
    if live:
        config['route_dicts'][-1]['title'] = add_args_to_title(title, [*args],
                                                    script=script)

def run(host='0.0.0.0', port=5000):
    """ Starts the Flask server """
    if not app:
        raise RuntimeError('Routes must be created before starting server.')
    app.run(host=host, port=port)
