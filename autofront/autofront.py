""" Main module for autofront, the automatic front-end

This module lets users start a simple one-page Flask server from which
they can trigger functions and scripts and see the result of their
print calls and return values in the browser. It also replaces regular
input calls with a version that gets user input in the browser.

Here is the basic usage::

    import autofront
    from my_module import my_function

    autofront.add(my_function)

    autofront.run()

That's all the code needed for a simple function with no arguments.

To add a route to a script::

    autofront.add('my_script.py')

To add a route with fixed arguments::

    autofront.add(my_function, 'arg1', 'arg2', kwarg1='bar')

To add a route with args input in browser at runtime::

    autofront.add(my_function, live=True)

To add a route with live args using type indications::

    autofront.add(my_function, live=True, typed=True)

To add a second route to the same function or script::
    autofront.add(my_function, title = new_name)

To add a route to a function or script meant to run in the background::
    autofront.add(my_function, join=False)

NOTE: Routes are not strictly speaking the same as Flask routes. Flask routes
connect an actual URL to a view function. An autofront routes is simply
a dictionary that contains the information autofront.functions needs
to know which function or script to trigger when the user selects
its representation in the browser, as well as the options to run it properly.

Scripts should be detected automatically. If detection fails, you can specify
the script kwarg::
    autofront.add('my_script.py', script=True)

If your function doesn't use input calls, set join to True to speed it up::
    autofront.add(my_function, join=False)

You can configure certain options with autofront.initialize (see function docstring).
This must be done before creating any routes, otherwise the server will be initialized
automatically using default options.

See the autofront wiki at "https://github.com/JimmyLamothe/autofront/wiki"
for more detailed information.
"""
import multiprocessing
from flask import Flask, redirect, render_template, request, url_for
from autofront.config import config, status, print_config_dict
from autofront.detect import detect_script, key_in_kwargs
from autofront.input_utilities import clear_input, clear_prompt, get_input_args
from autofront.input_utilities import get_input_kwargs, get_prompt
from autofront.input_utilities import initialize_prompt, put_input_args
from autofront.input_utilities import wait_for_prompt, write_input
from autofront.multi import cleanup_workers, create_process
from autofront.parse import TYPE_ERROR_MESSAGE
from autofront.utilities import add_args_to_title, check_for_main, cleanup
from autofront.utilities import clear_display, create_local_dir, create_local_script
from autofront.utilities import get_display, get_fixed_args, get_function
from autofront.utilities import get_live_args, get_local_ip, get_script_path, get_timeout
from autofront.utilities import is_live, is_script, needs_input, print_exception
from autofront.utilities import print_route_dicts, remove_args, set_main_process_pid
from autofront.utilities import set_python_command, title_exists, typed_args
from autofront.utilities import wait_to_join

app = None # This will be a Flask server created by initialize().

def functions():
    """ Main page displaying all functions and their print calls """
    #print_route_dicts() #Uncomment to check route dicts during development
    #print_config_dict() #Uncomment to check config dict during devellopment
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
                live_args = get_live_args(request, script=True)
                if live_args:
                    args += live_args
            if needs_input(title): #For scripts with input calls
                initialize_prompt()
                put_input_args(title, args)
                return redirect(url_for('browser_input', title=title))
            script_path = create_local_script(script_path)
            print('Creating process for {}'.format(remove_args(title)))
            create_process(script_path, *args, type='script', join=join,
                           timeout=timeout)
            return redirect(url_for('functions'))
        function = get_function(title) #Path for function calls
        fixed_args = get_fixed_args(title)
        args = fixed_args[0]
        kwargs = fixed_args[1]
        if is_live(title): #For functions with args input in browser
            typed = typed_args(title)
            live_args = get_live_args(request, typed=typed)
            if live_args[0] == 'Parsing Error':
                print_exception(live_args[1])
                display = get_display() + TYPE_ERROR_MESSAGE
                status['request_completed'] = True
                clear_display()
                route_dicts = config['route_dicts']
                top = config['top']
                return render_template('functions.html', title='functions', top=top,
                                       display=display, route_dicts=route_dicts)
            if live_args[0]:
                args += live_args[0]
            kwargs.update(live_args[1])
        if needs_input(title): #For functions that use input calls
            initialize_prompt()
            put_input_args(title, args, kwargs=kwargs)
            return redirect(url_for('browser_input', title=title))
        print('Creating process for {}'.format(remove_args(title)))
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
    Step 4: Run when the function or script has terminated - returns
            to the main page and displays final results if any.
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
            script_path = create_local_script(script_path)
            print('creating process for {}'.format(remove_args(title)))
            create_process(script_path, *args, type='input_script', join=False,
                           timeout=timeout)
            wait_for_prompt()
            return redirect(url_for('browser_input', title=title))
        function = get_function(title) #Function path
        args = get_input_args(title)
        kwargs = get_input_kwargs(title)
        print('creating process for {}'.format(remove_args(title)))
        create_process(function, *args, type='input_function', join=False,
                       timeout=timeout, **kwargs)
        wait_for_prompt()
        return redirect(url_for('browser_input', title=title))
    #STEP 4 - Script or function has finished running - Return to main page
    if prompt in ['finished', 'timeout reached']:
        return redirect(url_for('functions'))
    #STEP 2 - Script or function running - get input in browser
    if prompt == 'None':
        prompt = ''
    return render_template('web_input.html', title='get_input',
                           display=display, prompt=prompt)

def initialize(name=__name__, print_exceptions=True, template_folder=None,
               static_folder=None, timeout=30, top=False, worker_limit=20):
    """ Initialize the Flask app and clear the display. Running this after
    a route is added will raise an exception.

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
    if not check_for_main():
        return
    create_local_dir()
    cleanup()
    multiprocessing.set_start_method('spawn') #For consistency with 3.8 and Windows
    set_main_process_pid()
    set_python_command()
    config['print_exceptions'] = print_exceptions
    config['timeout'] = timeout
    config['top'] = top
    config['worker_limit'] = worker_limit
    clear_display()
    global app
    if template_folder and static_folder:
        app = Flask(name, template_folder=template_folder,
                    static_url_path=static_folder)
        print('Using custom static folder at {}'.format(str(static_folder)))
        print('Using custom template folder at {}'.format(str(template_folder)))
    elif template_folder:
        app = Flask(name, template_folder=template_folder)
        print('Using custom template folder at {}'.format(str(template_folder)))
    elif static_folder:
        app = Flask(name, static_folder=static_folder)
        print('Using custom static folder at {}'.format(str(static_folder)))
    else:
        app = Flask(name)
    app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])
    app.add_url_rule('/browser_input/<title>', 'browser_input',
                     browser_input, methods=['GET', 'POST'])

def initialize_default():
    """ Initializes the flask server with deault settings """
    print('Initializing server with default settings.')
    print('Run autofront.initialize() before adding routes to ' +
          'set optional settings.')
    initialize()

def add(function_or_script_path, *args, live=False, timeout=None,
                 title=None, typed=False, **kwargs):
    """ Create a new route to a function or script

    If you need to specify server options, this must be done with initialize before
    creating the first route.

    Usage is explained in the wiki at https://github.com/JimmyLamothe/autofront/wiki
    and in the main module doc string.

    Specify a title in the kwargs if you want a custom string displayed
    in the browser instead of your function name or script filename.

    Each function or script must have a different title. By default, the title
    is equal to the name of the function or script. You must use the title kwarg
    if you need two routes to the same function or script.

    Use join=True if you want to let your function finish running and you
    do not use input calls. This speeds up performance.

    Use join=False for functions or scripts meant to run in the background.
    Functions and scripts with input calls cannot run in the background,
    as autofront has no way of knowing which was the final input call
    until the function or script has finished execution.

    Do not specify the join kwarg if your function uses input calls, otherwise
    the input flow will be bypassed completely and it will appear to do nothing.

    Use live=True to input args at runtime (can be combined with fixed args).

    Use typed=True to use type indications in your live args.

    Use script=True if detection fails to identify a script

    Specify a timeout value (timeout=...) if a script of function hangs
    and needs to be stopped automatically.
    """
    if not check_for_main():
        return
    if not app:
        initialize_default()
    if not key_in_kwargs('script', **kwargs):
        script = detect_script(function_or_script_path)
    else:
        script = kwargs['script']
        del kwargs['script']
    if script:
        script_path = function_or_script_path
        function = None
        name = script_path
        if not key_in_kwargs('join', **kwargs):
            input_call = True #Default behavior
            join = False
        else:
            input_call = False
            join = kwargs['join']
            del kwargs['join']
    else:
        function = function_or_script_path
        script_path = None
        name = function.__name__
        if not key_in_kwargs('join', **kwargs):
            input_call = True
            join = False
        else:
            input_call = False
            join = kwargs['join']
            del kwargs['join']
    if not title:
        title = name
    if title_exists(title):
        message = 'A route with this title already exists.\n'
        message += 'Please specify a new title with the title kwarg.\n'
        message += "Example: autofront.add(my_function, title='new_title')\n"
        raise ValueError(message)
    link = title
    if not timeout:
        if join:
            timeout = config['timeout']
        else:
            timeout = None #These functions need to keep running in background
    config['route_dicts'].append({'function':function, #None if script
                                  'script':script, #True if script, False if function
                                  'script_path':script_path, #None if function
                                  'args':[*args],
                                  'kwargs':{**kwargs},
                                  'typed':typed,
                                  'link':link,
                                  'title':title,
                                  'live':live,
                                  'input':input_call,
                                  'join':join,
                                  'timeout':timeout})
    if live:
        config['route_dicts'][-1]['title'] = add_args_to_title(title, [*args],
                                                               script=script)

def run(host='0.0.0.0', port=5000):
    """ Starts the Flask server

    The host and port kwargs are managed by Flask. You can check the Flask docs
    if you want to modify them for any reason. You could theoretically use them
    to access your autofront server from outside your network, but this is not
    recommended as the standard Flask server is not designed to be safe from hacking.
    Future versions of autofront should allow you to deploy your autofront app
    to cloud servers such as Python Anywhere, giving you similar functionality
    without putting you at risk.
    """
    if not check_for_main():
        return
    if not app:
        raise RuntimeError('Routes must be created before starting server.')
    try:
        local_ip = get_local_ip()
        ip_port = local_ip + ':' + str(port)
        print('\n')
        print('Starting server. Access it from a local browser at localhost:5000')
        print('or a browser on the same local network at {}'.format(ip_port))
        print('\n')
    except Exception: #General exception for safety since autofront can run anyway
        print('\n')
        print('Starting server. Access it from a local browser at localhost:5000')
        print('or a browser on the same local network at your local IP on port 5000')
        print('\n')
    app.run(host=host, port=port)
