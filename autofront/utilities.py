import string

def get_function(func_title, func_dicts):
    functions = [func_dict for func_dict in func_dicts
                 if func_dict['title'] == func_title]
    if len(functions) > 1:
        raise Exception('Cannot use same title for your functions')
    else:
        func_dict = functions[0]
        function = func_dict['func']
        return function

def strip_spaces(input):
    return input.replace(' ', '')

def parse_kwargs(kwarg_list):
    kwargs = {}
    for kwarg in kwarg_list:
        kwarg = strip_spaces(kwarg)
        key_value = kwarg.split('=')
        key = key_value[0]
        value = key_value[1]
        kwargs[key] = value
    return kwargs

def parse_args(arg_string):
    arg_string = strip_spaces(arg_string)
    arg_list = arg_string.split(sep=',')
    args = []
    kwargs = []
    for arg in arg_list:
        if '=' in arg:
            kwargs.append(arg)
        else:
            args.append(arg)
    
    kwargs = parse_kwargs(kwargs)
    all_args = [args, kwargs]
    return all_args
