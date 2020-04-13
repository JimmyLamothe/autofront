import sys
from flask import Flask, redirect, url_for, render_template, request
#from autofront.decorators import redirect_print, display_path
from autofront.utilities import redirect_print, clear_display, get_display
from autofront.utilities import initialize, run_script, add_args_to_title
from autofront.utilities import get_function, get_args, get_fixed_args
from autofront.utilities import live_script

print('Development version active')

app = initialize(__name__)

func_dicts = [] 

def functions():
    print('running functions')
    if request.method =='POST':
        func_name = list(request.form.keys())[0]
        if live_script(func_name, func_dicts):
            clear_display()
            script = func_name[:-2]
            args = get_args(request, func_name, func_dicts)[0]
            run_script(script, *args)()
            return redirect(url_for('functions'))
        function = get_function(func_name, func_dicts)
        live_args = get_args(request, func_name, func_dicts)
        fixed_args = get_fixed_args(func_name, func_dicts)
        args = fixed_args[0] + live_args[0]
        kwargs = live_args[1]
        kwargs.update(fixed_args[1])
        clear_display()
        @redirect_print
        def wrapper():
            function(*args, **kwargs)
        wrapper.__name__ = function.__name__
        wrapper()
        return redirect(url_for('functions'))
    display = get_display()
    return render_template('functions.html', title = 'functions',
                           display = display, func_dicts = func_dicts)

app.add_url_rule('/', 'functions', functions, methods=['GET', 'POST'])


def create_route(function, *args, link = None, title = None,
                 live = False, script = False, **kwargs):
    if script == 'DONE':
        pass
    elif script:
        if not live:
            create_route(run_script(function, *args), *args, link = link,
                         title = title, live = live, script = 'DONE',
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
                function(*args, **kwargs)
        wrapper.__name__ = func_name
        wrapper()
        return redirect(url_for('functions'))
    app.add_url_rule('/' + link, link, new_route)
    func_dicts.append({'func': function,
                       'link':link,
                       'title':title,
                       'live':live,
                       'script':script})
    if live:
        func_dicts[-1]['args'] = [*args]
        func_dicts[-1]['kwargs'] = {**kwargs}
        func_dicts[-1]['title'] = add_args_to_title(title, [*args])
    
def run(host='0.0.0.0', port = 5000):
    app.run(host = host, port = port)
