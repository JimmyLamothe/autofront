from autofront.debug import debug_manager

@debug_manager
def parse_bool(arg):
    if arg == 'True':
        return True
    elif arg == 'False':
        return False
    else:
        raise ValueError('Correct format for boolean type is ' +
                         '"bool:True" or "bool:False"')

@debug_manager
def parse_string(arg):
    return arg

@debug_manager
def parse_int(arg):
    return int(arg)

@debug_manager
def parse_float(arg):
    return float(arg)

@debug_manager
def parse_complex(arg):
    return complex(arg)

@debug_manager
def parse_list(arg):
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    arg_list = split_type_args(arg_string)
    parsed_list = parse_type_arg_list(arg_list)
    return parsed_list

@debug_manager
def parse_tuple(arg):
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    arg_list = split_type_args(arg_string)
    parsed_list = parse_type_arg_list(arg_list)
    return tuple(parsed_list)

@debug_manager
def get_type(type_arg):
    return type_arg.partition(':')[0].strip(' ')

@debug_manager
def get_arg(type_arg):
    return type_arg.partition(':')[2]

@debug_manager
def create_dict(arg_string):
    print('create_dict from : ' + arg_string)
    new_dict = {}
    arg_list = split_type_args(arg_string)
    print('arg list : ' + str(arg_list))
    for arg in arg_list:
        key_value = arg.partition(' : ')
        key = key_value[0]
        value = key_value[2]
        key = parsing_functions[get_type(key)](get_arg(key))
        value = parsing_functions[get_type(value)](get_arg(value))
        new_dict[key] = value
    return new_dict

@debug_manager
def parse_dict(arg):
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    new_dict = create_dict(arg_string)
    return new_dict

@debug_manager
def get_char_indexes(arg_string, target):
    indexes = [index for index, char in enumerate(arg_string)
                  if char == target]
    return indexes

@debug_manager
def get_first_index(arg_string, target):
    indexes = get_char_indexes(arg_string, target)
    try:
        return indexes[0]
    except:
        return None

@debug_manager
def get_last_index(arg_string, target):
    indexes = get_char_indexes(arg_string, target)
    try:
        return indexes[-1]
    except:
        return None

@debug_manager
def get_list_indexes(arg_string):
    list_starts = get_char_indexes(arg_string, '[')
    list_ends = get_char_indexes(arg_string, ']')
    list_indexes = list(zip(list_starts, list_ends))
    return list_indexes

@debug_manager
def get_tuple_indexes(arg_string):
    tuple_starts = get_char_indexes(arg_string, '(')
    tuple_ends = get_char_indexes(arg_string, ')')
    tuple_indexes = list(zip(tuple_starts, tuple_ends))
    return tuple_indexes

@debug_manager
def get_dict_indexes(arg_string):
    dict_starts = get_char_indexes(arg_string, '{')
    dict_ends = get_char_indexes(arg_string, '}')
    dict_indexes = list(zip(dict_starts, dict_ends))
    return dict_indexes

@debug_manager
def get_banned_ranges(indexes_list):
    banned_ranges = []
    for indexes in indexes_list:
        banned_ranges += list(range(indexes[0],indexes[1]))
    return banned_ranges

@debug_manager
def get_banned_indexes(arg_string):
    list_indexes = get_list_indexes(arg_string)
    tuple_indexes = get_tuple_indexes(arg_string)
    dict_indexes = get_dict_indexes(arg_string)
    banned_indexes = []
    banned_indexes += get_banned_ranges(list_indexes)
    banned_indexes += get_banned_ranges(tuple_indexes)
    banned_indexes += get_banned_ranges(dict_indexes)
    return banned_indexes

@debug_manager
def get_colon_indexes(arg_string):
    colon_list = [index for index, char in enumerate(arg_string)
                  if char == ':']
    return colon_list

@debug_manager
def split_indexes(arg_string):
    start = 0
    comma_indexes = get_char_indexes(arg_string, ',')
    if not comma_indexes:
        return []
    split_indexes = []
    banned_indexes = get_banned_indexes(arg_string)
    for comma_index in comma_indexes:
        if comma_index not in banned_indexes:
            split_indexes.append(comma_index)
    return split_indexes

@debug_manager
def split_type_args(arg_string):
    split_list = split_indexes(arg_string)
    arg_list = []
    start = 0
    for index in split_list:
        arg_list.append(arg_string[start:index])
        start = index + 1
        while arg_string[start] == ' ':
            start += 1
    arg_list.append(arg_string[start:len(arg_string)])
    return arg_list
        
parsing_functions = {'bool' : parse_bool,
                     'str' : parse_string,
                     'int' : parse_int,
                     'float' : parse_float,
                     'complex' : parse_complex,
                     'list' : parse_list,
                     'tuple' : parse_tuple,
                     'dict' : parse_dict}

@debug_manager
def parse_type_arg(type_arg_string):
    type = get_type(type_arg_string)
    arg = get_arg(type_arg_string)
    return parsing_functions[type](arg)

@debug_manager    
def parse_type_arg_list(arg_list):
    parsed_list = []
    for arg in arg_list:
        parsed_list.append(parse_type_arg(arg))
    return parsed_list

@debug_manager
def parse_type_kwargs(kwarg_list):
    kwargs = {}
    for kwarg in kwarg_list:
        key_value = kwarg.split('=')
        key = key_value[0]
        key = strip_surrounding_spaces(key)
        key = parse_type_arg(key)
        value = key_value[1]
        value = strip_surrounding_spaces(value)
        value = parse_type_arg(value)
        kwargs[key] = value
    return kwargs

@debug_manager
def parse_type_args(arg_string):
    kwargs = {}
    kwarg_start = None
    kwarg_middle = get_first_index(arg_string, '=')
    if kwarg_middle:
        kwarg_start = get_last_index(arg_string[0:kwarg_middle], ',') + 1
    if kwarg_start:
        kwarg_string = strip_surrounding_spaces(arg_string[kwarg_start:])
        arg_string = strip_surrounding_spaces(arg_string[:kwarg_start -1])
        kwarg_list = kwarg_string.split(sep=',')
        kwargs = parse_type_kwargs(kwarg_list)
    print('arg_string: ' + arg_string)
    arg_list = split_type_args(arg_string)
    print('arg_list: ' + str(arg_list))
    parsed_args = parse_type_arg_list(arg_list)
    all_args = [parsed_args, kwargs]
    return all_args

@debug_manager
def strip_surrounding_spaces(input):
    if input[0] == ' ':
        input = input[1:]
    if input[-1] == ' ':
        input = input[:-1]
    return input

@debug_manager
def parse_kwargs(kwarg_list):
    kwargs = {}
    for kwarg in kwarg_list:
        key_value = kwarg.split('=')
        key = key_value[0]
        key = strip_surrounding_spaces(key)
        value = key_value[1]
        value = strip_surrounding_spaces(value)
        kwargs[key] = value
    return kwargs

@debug_manager
def parse_args(arg_string):
    arg_string = strip_surrounding_spaces(arg_string)
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
