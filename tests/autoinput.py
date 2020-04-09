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

from simple_function import foo, bar, positional, keywords, combined

autofront.create_route(foo)

autofront.create_route(bar)

autofront.create_live_route(positional)

autofront.create_live_route(keywords)

autofront.create_live_route(combined)

autofront.run()
