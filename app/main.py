import sys


def main():
    # Uncomment this block to pass the first stage


    

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        user_command = input()

        args = user_command.split(" ")
        if args[0] == "exit":
            if args[1] == "0":
                sys.exit(0)
        elif args[0] == "echo":
            print(user_command[len("echo "):])
        else:
            print(f"{user_command}: command not found")
        
        
            

if __name__ == "__main__":
    main()
