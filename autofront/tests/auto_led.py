import autofront
from remote_led import flash_led

autofront.initialize()

autofront.create_route(flash_led, live=True, typed=True)

autofront.run()
