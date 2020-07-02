import pathlib

config = {'local_path':pathlib.Path(__file__).parent.joinpath('local'),
          'print_exceptions':True,
          'route_dicts':[],
          'timeout':5,
          'worker_limit':20}

