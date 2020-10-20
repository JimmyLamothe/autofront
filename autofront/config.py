""" Configuration module

This module contains all the route dictionaries created with autofront.create_route
as well as general configuration parameters. Most of the configuration parameters
can be modified when initializing the server using kwargs with autofront.initialize.

'print_exceptions' displays most route exceptions in the browser instead of the console
'route_dicts' stores all the route dictionaries created with autofront.create_route
'top' specifies whether to print route results at the top or bottom of the display
'timeout' determines the default timeout value for workers in case they hang
'worker_limit' sets a maximum number of active workers above which autofront assumes
a bug has occured and multi.cleanup_workers can eliminate the oldest workers.

The default values defined here should match the default values of the
autofront.initialize kwargs, but this is only for clarity when reading the code.
The values specified here will be overridden when autofront.initialize is executed,
either by the default kwargs or the ones specified by the user.
"""

config = {'print_exceptions':True,
          'route_dicts':[],
          'top':False,
          'timeout':60,
          'worker_limit':20}

status = {'request_received':False,
          'waiting':False,
          'request_completed':False}
