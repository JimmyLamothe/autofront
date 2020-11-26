import autofront

def delayed_print(string):
    import time
    time.sleep(4)
    autofront.utilities.print_to_display(string)

autofront.create_route(delayed_print, live=True, join=False)
autofront.create_route(autofront.get_display)

autofront.run()
