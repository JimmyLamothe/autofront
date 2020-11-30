import autofront
from remote_led import flash_led

autofront.add(flash_led, live=True, typed=True)

autofront.run()
