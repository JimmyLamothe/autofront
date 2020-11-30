import autofront

def delayed_print(string):
    import time
    time.sleep(4)
    autofront.utilities.print_to_display(string)

autofront.add(delayed_print, live=True, join=False)
autofront.add(autofront.get_display)

autofront.run()
