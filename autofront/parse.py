"""Parsing functions for argument strings

This module is used to parse argument strings into a list
of individual arguments. Only parse_args and parse_type_args
are called from outside the  module.

parse_args interprets all arguments to be of type str.
This is anticipated to be the default usage to get variables
from user input, which can be interpreted by the calling function
as necessary. At the moment the following
characters cannot be used in a string because an escape functionality
has not been implemented: , =

parse_type_args is used to parse argument strings with type indications.

Here is the required format to specify types:

The following arguments:

True, [3, '4'], foo={bar : (3.4, 4)}

must be input as:

bool:True, list:[int:3, str:4],
str:foo = dict:{str:bar : tuple:(float:3.4, int:4)}

Make sure to open and close all lists, tuples and dicts as usual.

Every argument must be preceded by the type and a colon.
Keys and values in dicts must be separated by a colon
with spaces around it.

Presently the following types are implemented:

bool - str - int - float - complex - list - tuple - dict

To understand the parsing method, it's recommended to step through
an example using the debug manager to follow the parsing logic.
"""

from autofront.debug import debug_manager

@debug_manager
def parse_bool(arg):
    """parses boolean arguments | str --> bool"""
    if arg == 'True':
        return True
    elif arg == 'False':
        return False
    else:
        raise ValueError('Correct format for boolean type is ' +
                         '"bool:True" or "bool:False"')

@debug_manager
def parse_string(arg):
    """parses string arguments | str --> str"""
    escaped_indexes = get_escaped_indexes(arg)
    if escaped_indexes:
        parsed = ''
        escape_characters = [index -1 for index in escaped_indexes]
        start = 0
        for index in escape_characters:
            parsed += arg[start:index]
            start = index + 1
        parsed += arg[start:]
        return parsed
    return arg

@debug_manager
def parse_int(arg):
    """parses integer arguments | str --> int"""
    return int(arg)

@debug_manager
def parse_float(arg):
    """parses float arguments | str --> float """
    return float(arg)

@debug_manager
def parse_complex(arg):
    """parses complex arguments | str --> complex"""
    return complex(arg)

@debug_manager
def parse_list(arg):
    """parses lists | str --> list"""
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    arg_list = split_type_args(arg_string)
    parsed_list = parse_type_arg_list(arg_list)
    return parsed_list

@debug_manager
def parse_tuple(arg):
    """parses tuples | str --> tuple"""
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    arg_list = split_type_args(arg_string)
    parsed_list = parse_type_arg_list(arg_list)
    return tuple(parsed_list)

@debug_manager
def create_dict(arg_string):
    """creates a dict - called from parse_dict | str --> dict"""
    new_dict = {}
    arg_list = split_type_args(arg_string)
    for arg in arg_list:
        key_value = arg.partition(' : ')
        key = key_value[0]
        value = key_value[2]
        key = PARSING_FUNCTIONS[get_type(key)](get_arg(key))
        value = PARSING_FUNCTIONS[get_type(value)](get_arg(value))
        new_dict[key] = value
    return new_dict

@debug_manager
def parse_dict(arg):
    """parses dicts | str --> dict"""
    arg_string = strip_surrounding_spaces(arg)[1:-1]
    new_dict = create_dict(arg_string)
    return new_dict

@debug_manager
def get_type(type_arg):
    """get the type from type:arg format | str --> str"""
    return type_arg.partition(':')[0].strip(' ')

@debug_manager
def get_arg(type_arg):
    """get the argument from type:arg format | str --> str"""
    return type_arg.partition(':')[2]

@debug_manager
def get_char_indexes(arg_string, target):
    """list all instances of char in string | str --> list(int)"""
    indexes = [index for index, char in enumerate(arg_string)
               if char == target]
    return indexes

#Replicates str.find - returns None on failure
@debug_manager
def get_first_index(arg_string, target):
    """get first instance of char in string | str --> int"""
    indexes = get_char_indexes(arg_string, target)
    try:
        return indexes[0]
    except IndexError:
        return None

#Replicates str.rfind - returns None on failure
@debug_manager
def get_last_index(arg_string, target):
    """get last instance of char in string | str --> int"""
    indexes = get_char_indexes(arg_string, target)
    try:
        return indexes[-1]
    except IndexError:
        return None

@debug_manager
def get_list_indexes(arg_string):
    """Find list start and end indexes | str --> list(tuple)"""
    list_starts = get_char_indexes(arg_string, '[')
    list_ends = get_char_indexes(arg_string, ']')
    list_indexes = list(zip(list_starts, list_ends))
    return list_indexes

@debug_manager
def get_tuple_indexes(arg_string):
    """Find tuple start and end indexes | str --> list(tuple)"""
    tuple_starts = get_char_indexes(arg_string, '(')
    tuple_ends = get_char_indexes(arg_string, ')')
    tuple_indexes = list(zip(tuple_starts, tuple_ends))
    return tuple_indexes

@debug_manager
def get_dict_indexes(arg_string):
    """Find dict start and end indexes | str --> list(tuple)"""
    dict_starts = get_char_indexes(arg_string, '{')
    dict_ends = get_char_indexes(arg_string, '}')
    dict_indexes = list(zip(dict_starts, dict_ends))
    return dict_indexes

@debug_manager
def get_banned_ranges(indexes_list):
    """Get range from start and end indexes | list(tuples) --> list(int)"""
    banned_ranges = []
    for indexes in indexes_list:
        banned_ranges += list(range(indexes[0], indexes[1]))
    return banned_ranges

ESCAPED_CHARS = [',', '='] #Might add more if needed for parsing

@debug_manager
def get_escaped_indexes(arg_string):
    """ Get indexes of characters in ESCAPED_CHARS | str -->list(int) """
    escape_indexes = get_char_indexes(arg_string, '\\')
    if arg_string[-1] == '\\': #Can't be followed by special char
        escape_indexes = escape_indexes[:-1]
    escaped_indexes = [index + 1 for index in escape_indexes
                       if arg_string[index + 1] in ESCAPED_CHARS]
    return escaped_indexes

@debug_manager
def get_banned_indexes(arg_string):
    """Get indexes inside lists - tuples - dicts | str --> list(int)

    Note: This will also get these characters when used
    in words and phrases inside strings, but this is not a problem
    as the point is to avoid splitting argument in the wrong place.
    Having extra banned indexes is fine. This also gets the index
    of escaped commas in type(str) arguments to avoid splitting there..
    """
    list_indexes = get_list_indexes(arg_string)
    tuple_indexes = get_tuple_indexes(arg_string)
    dict_indexes = get_dict_indexes(arg_string)
    banned_indexes = []
    banned_indexes += get_banned_ranges(list_indexes)
    banned_indexes += get_banned_ranges(tuple_indexes)
    banned_indexes += get_banned_ranges(dict_indexes)
    banned_indexes += get_escaped_indexes(arg_string)
    return banned_indexes

@debug_manager
def get_colon_indexes(arg_string):
    """Get indexes of all colons | str --> list(int)"""
    colon_list = [index for index, char in enumerate(arg_string)
                  if char == ':']
    return colon_list

@debug_manager
def get_split_indexes(arg_string):
    """Find indexes to split string into arguments | str --> list(int)"""
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
    """Split argument string into individual args | str --> list(str)"""
    split_list = get_split_indexes(arg_string)
    arg_list = []
    start = 0
    for index in split_list:
        arg_list.append(arg_string[start:index])
        start = index + 1
        while arg_string[start] == ' ':
            start += 1
    arg_list.append(arg_string[start:len(arg_string)])
    return arg_list

PARSING_FUNCTIONS = {'bool' : parse_bool,
                     'str' : parse_string,
                     'int' : parse_int,
                     'float' : parse_float,
                     'complex' : parse_complex,
                     'list' : parse_list,
                     'tuple' : parse_tuple,
                     'dict' : parse_dict}

@debug_manager
def parse_type_arg(type_arg_string):
    """Parse typed individual argument strings

    This is the base function to parse an individual argument
    string with type information. It identifies the type and calls
    the appropriate parsing function from the parsing function dict.

    Args:
        type_arg_string(str): Typed argument in string form

    Returns:
        argument with correct type

    """

    arg_type = get_type(type_arg_string)
    arg = get_arg(type_arg_string)
    return PARSING_FUNCTIONS[arg_type](arg)

@debug_manager
def parse_type_arg_list(arg_list):
    """Calls parse_type_arg on all args in list | list(str) --> list"""
    parsed_list = []
    for arg in arg_list:
        parsed_list.append(parse_type_arg(arg))
    return parsed_list

@debug_manager
def parse_type_kwargs(kwarg_list):
    """Parses typed keyword arguments | list(str) --> dict"""
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
def get_first_kwarg_equal(arg_string):
    """ Find first kwarg equal sign | str --> int or None """
    escaped_indexes = get_escaped_indexes(arg_string)
    kwarg_equal_indexes = get_char_indexes(arg_string, '=')
    kwarg_equal_indexes = [index for index in kwarg_equal_indexes
                           if not index in escaped_indexes]
    if not kwarg_equal_indexes:
        return None
    return kwarg_equal_indexes[0]

@debug_manager
def get_arg_bool(arg_string):
    """ Check if there are *args in arg_string | str --> bool """
    if not arg_string: #If no arguments were passed
        return False
    first_kwarg_equal = get_first_kwarg_equal(arg_string)
    if first_kwarg_equal:
        escaped_indexes = get_escaped_indexes(arg_string)
        arg_end = get_char_indexes(arg_string[0:first_kwarg_equal], ',')
        arg_end = [index for index in arg_end
                   if not index in escaped_indexes]
        if arg_end: #If non-escaped comma, *args exist
            return True
        return False
    return True #If arg_string but no kwargs, *args exist

@debug_manager
def get_kwarg_bool(arg_string):
    """ Check if there are **kwargs in arg_string | str --> bool """
    if not arg_string: #If no arguments were passed
        return False
    first_kwarg_equal = get_first_kwarg_equal(arg_string)
    if first_kwarg_equal: #If non-escaped equal sign, **kwargs exist
        return True
    return False # If arg_string but no equal sign, no **kwargs

@debug_manager
def parse_type_args(all_arg_string):
    """ Parse typed argument string

    Called from outside module. Parses an argument string possibly
    containing multiple arguments in a specific format.

    See module docs for more info.

    Args:
        arg_string(str): A string of typed arguments

    Returns:
        list: A list of arguments and keyword arguments
              with the correct type.
    """

    all_arg_string = strip_surrounding_spaces(all_arg_string)
    arg_bool = get_arg_bool(all_arg_string)
    kwarg_bool = get_kwarg_bool(all_arg_string)
    if not kwarg_bool and not arg_bool:
        all_args = [[], {}] # No arguments passed
    elif arg_bool and kwarg_bool:
        first_kwarg_equal = get_first_kwarg_equal(all_arg_string)
        kwarg_start = get_last_index(
            all_arg_string[0:first_kwarg_equal], ',') + 1
        arg_string = strip_surrounding_spaces(
            all_arg_string[:kwarg_start -1])
        kwarg_string = strip_surrounding_spaces(
            all_arg_string[kwarg_start:])
    elif arg_bool and not kwarg_bool:
        arg_string = all_arg_string
        kwarg_string = None
    else:
        arg_string = None
        kwarg_string = all_arg_string
    if kwarg_string: #If kwargs
        kwarg_list = split_type_args(kwarg_string)
        parsed_kwargs = parse_type_kwargs(kwarg_list)
    else:
        parsed_kwargs = {}
    if arg_string: #If args
        arg_list = split_type_args(arg_string)
        parsed_args = parse_type_arg_list(arg_list)
    else:
        parsed_args = []
    all_args = [parsed_args, parsed_kwargs]
    return all_args

@debug_manager
def strip_surrounding_spaces(string):
    """Strip leading and trailing space | str --> str"""
    if string == '':
        return string
    if string[0] == ' ':
        string = string[1:]
    if string[-1] == ' ':
        string = string[:-1]
    return string


#Used for non-typed argument strings
@debug_manager
def parse_kwargs(kwarg_list):
    """Creates kwarg dict from list of kwargs | list(str) --> dict"""
    kwargs = {}
    for kwarg in kwarg_list:
        key_value = kwarg.split('=')
        key = key_value[0]
        key = strip_surrounding_spaces(key)
        value = key_value[1]
        value = strip_surrounding_spaces(value)
        kwargs[key] = value
    return kwargs

#Used for non-typed arguments strings
@debug_manager
def parse_args(arg_string):
    """Creates arg + kwarg list from arg string | str --> lst(lst(str))"""
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
