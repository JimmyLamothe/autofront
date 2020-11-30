import autofront
from simple_functions import foo

autofront.add(foo)

#autofront.add(foo) #Uncomment to test duplicate titles - should raise exception

autofront.add(foo, title='bar')

autofront.run()
