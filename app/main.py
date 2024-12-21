import sys
import os

builtin = ["echo","type", "exit"]


def handle_input(user_command):

    if "type" == user_command.split(" ")[0]:
        if user_command.split(" ")[1] in builtin:
            second_word = user_command.split(" ")[1]
            sys.stdout.write(f"{second_word} is a shell builtin\n")
        else:
            # sys.stdout.write(f"{user_command.split(" ")[1]} not found\n")
            paths = os.getenv("PATH").split(":")

            for path in paths:
                second_word = user_command.split(" ")[1]
                if os.path.exists(f"{path}/{second_word}"):
                    second_word = user_command.split(" ")[1]
                    sys.stdout.write(f"{second_word} is {path}/{second_word}\n")
                    break
            else:
                second_word = user_command.split(" ")[1]
                sys.stdout.write(f"{second_word} not found\n")
    elif user_command == "exit 0":
        return False
    elif "echo" == user_command.split(" ")[0]:
        invalid = user_command[len("echo "):]
        sys.stdout.write(f"{invalid}\n")
    else:
        sys.stderr.write(f"{user_command}: command not found\n")
        sys.stdout.flush()



def main():
    # Uncomment this block to pass the first stag
    

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        user_command = input()
        handle_response = handle_input(user_command)

        if handle_response == False:
            break
        
        
            

if __name__ == "__main__":
    main()
