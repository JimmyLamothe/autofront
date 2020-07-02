import sys

if len(sys.argv) == 2:
    user_input = input("Let's play match the arg! Input the arg you entered")
    if user_input == sys.argv[1]:
        print('You won!')
    else:
        print('You lost!')

elif len(sys.argv) == 1: #NOTE: Not actually possible with current implementation
    print("Can't play match the arg with no args!")

else:
    print("Can't play match the args with so many args!")
