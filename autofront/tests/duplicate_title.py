import autofront
from simple_functions import foo

autofront.create_route(foo)

#autofront.create_route(foo) #Uncomment to test duplicate titles - should raise exception

autofront.create_route(foo, title='bar')

autofront.run()
