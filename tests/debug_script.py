import pdb
import autofront

autofront.initialize()

autofront.create_route('simple_script_live.py', script=True, live=True)

pdb.run('autofront.run()')
