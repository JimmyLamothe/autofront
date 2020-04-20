""" Main module for autofront automatic front-end

This module lets users create routes to other functions and scripts
they've written. It starts a simple Flask server with one page from
where you can execute functions, see the result of their print calls
and see their return values in string form.

Here is the basic usage::

    import autofront
    from my_module import my_function

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

from flask import redirect, url_for, render_template, request
from autofront.utilities import redirect_print, clear_display, get_display
from autofront.utilities import initialize, run_script, add_args_to_title
from autofront.utilities import get_function, get_args, get_fixed_args
from autofront.utilities import live_script, typed_args, print_return_value

print('Development version active')

app = initialize(__name__)

func_dicts = []

def functions():
    """ Landing page displaying all functions and their print calls """
    print('running functions')
    if request.method == 'POST':
        func_name = list(request.form.keys())[0]
        if live_script(func_name, func_dicts):
            clear_display()
            script = func_name[:-2]
            args = get_args(request)[0]
            run_script(script, *args)()
            return redirect(url_for('functions'))
        function = get_function(func_name, func_dicts)
        typed = typed_args(func_name, func_dicts)
        live_args = get_args(request, typed=typed)
        fixed_args = get_fixed_args(func_name, func_dicts)
        args = fixed_args[0] + live_args[0]
        kwargs = live_args[1]
        kwargs.update(fixed_args[1])
        clear_display()
        @redirect_print
        def wrapper():
            return function(*args, **kwargs)
        wrapper.__name__ = function.__name__
        return_value = wrapper()
        print('return value : ' + str(return_value))
        if return_value:
            print_return_value(return_value)
        return redirect(url_for('functions'))
    display = get_display()
    return render_template('functions.html', title='functions',
                           display=display, func_dicts=func_dicts)

app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])


def create_route(function, *args, title=None, link=None, live=False,
                 script=False, typed=False, **kwargs):
    """ Function to create a new route to a function or script

    Usage is explained in docs and main module doc string.

    Use live=True for args input at runtime.

    Use script=True and the script path as the function positional arg
    to run a script instead of a function.

    Use typed=True to use type indications in your live args.

    Specify the title kwarg to display a specific string for your
    function in the browser.

    """
    if script == 'DONE':
        pass
    elif script:
        if not live:
            create_route(run_script(function, *args), *args, title=title,
                         link=link, live=live, typed=False, script='DONE',
                         **kwargs)
            return
        else:
            def temp():
                pass
            new_route = temp
    if not (script and live):
        func_name = function.__name__
    else:
        func_name = function
    print('args for ' + func_name + ': ' + str(args))
    print('kwargs for ' + func_name + ': ' + str(kwargs))
    if not link:
        link = func_name
    if not title:
        title = func_name
    def new_route():
        clear_display()
        if script == 'DONE':
            wrapper = function
        else:
            @redirect_print
            def wrapper():
                return function(*args, **kwargs)
        wrapper.__name__ = func_name
        return_value = wrapper()
        if return_value:
            print_return_value(return_value)
        return redirect(url_for('functions'))
    app.add_url_rule('/' + link, link, new_route)
    func_dicts.append({'func': function,
                       'link':link,
                       'title':title,
                       'live':live,
                       'script':script,
                       'typed':typed})
    if live:
        func_dicts[-1]['args'] = [*args]
        func_dicts[-1]['kwargs'] = {**kwargs}
        func_dicts[-1]['title'] = add_args_to_title(title, [*args])

def run(host='0.0.0.0', port=5000):
    """ Start Flask server """
    app.run(host=host, port=port)
