import sys
import os
import shlex
def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        paths = os.getenv("PATH").split(":")
        if command == "exit 0":
            break
        elif command == "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        elif command.startswith("cat"):
            command_list = shlex.split(command, posix=True)
            for index in range(1, len(command_list)):
                file_path = command_list[index]
                file = open(file_path, "r")
                sys.stdout.write(f"{file.read()}")
                file.close()
        elif command.startswith('"') or command.startswith("'"):
            command_list = shlex.split(command, posix=True)
            file_path = command_list[1]
            file = open(file_path, "r")
            sys.stdout.write(f"{file.read()}")
            file.close()
        elif command.startswith("cd"):
            command_list = command.split()
            cd_command_path = command_list[1]
            try:
                if cd_command_path.startswith("."):
                    cd_command_path = os.path.normpath(
                        os.path.join(os.getcwd(), cd_command_path)
                    )
                elif cd_command_path.startswith("~"):
                    cd_command_path = os.getenv("HOME")
                os.chdir(cd_command_path)
            except FileNotFoundError:
                sys.stdout.write(f"cd: {cd_command_path}: No such file or directory\n")
        elif command.startswith("echo"):
            command_list = shlex.split(command, posix=True)
            sys.stdout.write(f"{" ".join(command_list[1:])}\n")
        elif command.startswith("type"):
            command_list = command.split()
            type_command = command_list[1]
            valid_type_commands = ["echo", "exit", "type", "pwd", "cd"]
            if type_command in valid_type_commands:
                sys.stdout.write(f"{type_command} is a shell builtin\n")
            else:
                is_command_path_exists = False
                for path in paths:
                    if os.path.exists(f"{path}/{type_command}"):
                        sys.stdout.write(f"{type_command} is {path}/{type_command}\n")
                        is_command_path_exists = True
                        break
                if is_command_path_exists == False:
                    sys.stdout.write(f"{type_command}: not found\n")
        else:
            command_list = command.split()
            executable_command = command_list[0]
            is_command_path_exists = False
            for path in paths:
                if os.path.exists(f"{path}/{executable_command}"):
                    os.system(f"{path}/{command}")
                    is_command_path_exists = True
                    break
            if is_command_path_exists == False:
                sys.stdout.write(f"{executable_command}: command not found\n")
if __name__ == "__main__":
    main()