import sys
import os


def find_path(param):
    path = os.environ['PATH']
    for directory in path.split(":"):
        for (dirpath, dirnames, filenames) in os.walk(directory):
            if param in filenames:
                return f"{dirpath}/{param}"
    return None


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        user_command = input().strip()
        if not user_command:
            continue

        # Split the command into parts
        command_parts = user_command.split(" ")

        # Check for specific commands
        if command_parts[0] == "exit" and len(command_parts) > 1 and command_parts[1] == "0":
            exit(0)
        elif command_parts[0] == "echo":
            print(" ".join(command_parts[1:]))
        elif command_parts[0] == "type":
            if len(command_parts) > 1:
                cmd = command_parts[1]
                if cmd in ["echo", "type", "exit"]:
                    print(f"{cmd} is a shell builtin")
                else:
                    location = find_path(cmd)
                    if location:
                        print(f"{cmd} is {location}")
                    else:
                        print(f"{cmd} not found")
            else:
                print("type: missing argument")
        else:
            # Default behavior for unknown commands
            command_name = command_parts[0]
            if os.path.isfile(command_name):
                os.system(user_command)
            else:
                print(f"{user_command}: command not found")


if __name__ == "__main__":
    main()
