import sys, os, subprocess

my_env = os.environ
#my_env['FLASK_APP'] = 'test.py'
my_env['FLASK_APP'] = 'spot_play.py'

def start_server():
    try:
        subprocess.run(['flask', 'run'])
    except KeyboardInterrupt:
        exit = input('Input any key to exit, ENTER to restart server')
        if not exit:
            start_server()

start_server()

