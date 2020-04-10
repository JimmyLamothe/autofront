import sys
from flask import Flask, redirect, url_for, render_template, request
#from autofront.decorators import redirect_print, display_path
from autofront.utilities import redirect_print, clear_display, get_display
from autofront.utilities import initialize, run_script
from autofront.utilities import get_function, get_args

print('Development version active')

app = initialize(__name__)

func_dicts = [] #List of link address and link name for each function

#TO DO: Make multiple page formats - (choose layout, change title, etc)
def functions():
    if request.method =='POST':
        func_name = list(request.form.keys())[0]
        function = get_function(func_name, func_dicts)
        all_args = get_args(request, func_name, func_dicts)
        args = all_args[0]
        kwargs = all_args[1]
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
                 live = False, script = False, mixed_args = False,
                 **kwargs):
    if script == 'DONE':
        pass
    elif script:
        create_route(run_script(function, *args), *args, link = link,
                     title = title, live = live, script = 'DONE',
                     mixed_args = mixed_args, **kwargs)
        return
    func_name = function.__name__
    print('args for ' + func_name + ': ' + str(args))
    print('kwargs for ' + func_name + ': ' + str(kwargs))
    if not link:
        link = func_name
    if not title:
        title = func_name
    def new_route():
        clear_display()
        if mixed_args:
            pass
        elif script == 'DONE':
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
                       'script':script,
                       'mixed_args':mixed_args})
    if mixed_args:
        func_dicts[-1]['args'] = [*args]
        func_dicts[-1]['kwargs'] = {**kwargs}
    
def run(host='0.0.0.0', port = 5000):
    app.run(host = host, port = port)
