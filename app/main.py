import sys


def main():
    # Uncomment this block to pass the first stage


    

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        user_command = input()
        if user_command == "exit 0":
            break
        print(f"{user_command}: command not found")
            
        
            

if __name__ == "__main__":
    main()
