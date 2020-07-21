""" Configuration module

This module contains all the route dictionaries created with autofront.create_route
as well as general configuration parameters. Most of the configuration parameters
can be modified when initializing the server using kwargs with autofront.initialize.

'local_path' determines the path used to store and load temporary files
'print_exceptions' displays most route exceptions in the browser instead of the console
'route_dicts' stores all the route dictionaries created with autofront.create_route
'timeout' determines the default timeout value for workers in case they hang
'worker_limit' sets a maximum number of active workers above which autofront assumes
a bug has occured and multi.cleanup_workers can eliminate the oldest workers.

The default values dedfined here for timeout, print_exceptions and worker_limit
should match the ones in autofront.initialize kwargs, but this is only for clarity.
They will always be set by autofront.initialize. 

"""

import pathlib

config = {'local_path':pathlib.Path(__file__).parent.joinpath('local'),
          'print_exceptions':True, 
          'route_dicts':[],
          'top':False,
          'timeout':10,
          'worker_limit':20}

status = {'request_received':False,
          'waiting':False,
          'request_completed':False}
