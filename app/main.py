import os
import subprocess
import sys
from typing import Optional
def locate_executable(cmd) -> Optional[str]:
    path = os.environ.get("PATH", "")
    for directory in path.split(":"):
        file_path = os.path.join(directory, cmd)
        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path
def parse_command(input_line: str):
    def tokenize(line):
        token = []
        in_single_quotes = False
        in_double_quotes = False
        escape_next = False
        for char in line:
            # if char == "'" and not in_double_quotes:
            if escape_next:
                token.append(char)
                escape_next = False
                continue
            elif char == "\\":
                if in_single_quotes or in_double_quotes:
                    token.append(char)
                else:
                    escape_next = True
                continue
            elif char == "'" and not in_double_quotes:
                in_single_quotes = not in_single_quotes
            elif char == '"' and not in_single_quotes:
                in_double_quotes = not in_double_quotes
            elif char == " " and not in_single_quotes and not in_double_quotes:
                if token:
                    yield "".join(token)
                    token = []
            else:
                token.append(char)
        if token:
            yield "".join(token)
    return list(tokenize(input_line))
def handle_exit(args):
    sys.exit(int(args[0]) if args else 0)
def handle_echo(args):
    print(" ".join(args))
def handle_type(args):
    if args[0] in builtins:
        print(f"{args[0]} is a shell builtin")
    else:
        executable = locate_executable(args[0])
        if executable:
            print(f"{args[0]} is {executable}")
        else:
            print(f"{args[0]}: not found")
def handle_pwd(args):
    if args:
        if args[0] == "pwd":
            print("pwd is a shell builtin")
        else:
            print(f"pwd: invalid argument '{args[0]}'")
    else:
        print(os.getcwd())
def handle_cd(args):
    if len(args) != 1:
        print("cd: too many arguments")
        return
    path = args[0]
    if path.startswith("~"):
        path = os.path.expanduser(path)
    resolved_path = os.path.abspath(path)
    try:
        os.chdir(resolved_path)
    except FileNotFoundError:
        print(f"cd: {path}: No such file or directory")
    except NotADirectoryError:
        print(f"cd: {path}: Not a directory")
    except PermissionError:
        print(f"cd: {path}: Permission denied")
builtins = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}
def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        input_line = input()
        parsed_args = parse_command(input_line)
        if not parsed_args:
            continue
        cmd, *args = parsed_args
        if cmd in builtins:
            builtins[cmd](args)
            continue
        else:
            executable = locate_executable(cmd)
            if executable:
                subprocess.run([executable, *args])
            else:
                print(f"{cmd}: command not found")
        sys.stdout.flush()
if __name__ == "__main__":
    main()