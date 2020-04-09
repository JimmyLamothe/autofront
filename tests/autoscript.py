import sys

args = sys.argv

if len(args) > 1:
    if args[1] == 'dev':
        sys.path.insert(1, '/Users/jimmy/Programming/Python/autofront/')
        import autofront
    else:
        sys.exit('invalid argument')
else:
    import autofront

autofront.create_route(autofront.run_script('simple_script.py'))

autofront.run()
