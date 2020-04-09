import sys

args = sys.argv

print('It works!')

if len(args) == 1:
    print('But you forgot the args.')
    sys.exit(0)

else:
    args = args[1:]

print('Here are your args:')

for arg in args:
    print(arg)
