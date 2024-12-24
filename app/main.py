import os
import subprocess
import sys
from typing import Optional


BUILTINS = ["echo", "exit", "type", "pwd", "cd"]


def present_on_path(command) -> Optional[str]:
    path = os.environ.get("PATH")
    if path:
        dirs = path.split(":")
        for dir in dirs:
            full_path = os.path.join(dir, command)
            if os.path.isfile(full_path):
                return full_path
    return None


def handle_type(args):
    if args[0] in BUILTINS:
        print(f"{args[0]} is a shell builtin")
        return
    else:
        full_path = present_on_path(args[0])
        if full_path:
            print(f"{args[0]} is {full_path}")
            return
    print(f"{args[0]}: not found")

    
def normalise_args(user_input) -> list[str]:
    res = []
    arg = ""
    i = 0
    while i < len(user_input):
        if user_input[i] == "'":
            i += 1
            start = i
            while i < len(user_input) and user_input[i] != "'":
                i += 1
            res.append(user_input[start:i])
            arg += user_input[start:i]
            i += 1
        elif user_input[i] == '"':
            i += 1
            arg = ""
            while i < len(user_input):
                if user_input[i] == "\\":
                    if user_input[i + 1] in ["\\", "$", '"', "\n"]:
                        if user_input[i + 1] == "n":
                            arg += "\n"  # Handle newline escape
                        elif user_input[i + 1] == "t":
                            arg += "\t"  # Handle tab escape
                        else:
                            arg += user_input[i + 1]
                        i += 2
                    else:
                        arg += user_input[i]
                        i += 1
                elif user_input[i] == '"':
                    break
                else:
                    arg += user_input[i]
                    i += 1
            res.append(arg)
            i += 1
        elif user_input[i] == " ":
            if arg:
                res.append(arg)
            arg = ""
            i += 1
        elif user_input[i] == "\\":
            i += 1
        else:
            arg = ""
            while i < len(user_input) and user_input[i] != " ":
                if user_input[i] == "\\":
                    arg += user_input[i + 1]
                    i += 2
                else:
                    arg += user_input[i]
                    i += 1
            res.append(arg)
    if arg:
        res.append(arg)
    return res


def handle_echo(args):
    output = " ".join(args)
    processed_output = output.encode('utf-8').decode('unicode_escape')
    print(processed_output)


def main():
    cur_dir = os.getcwd()
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input()
        if not user_input.strip():
            continue
        args = normalise_args(user_input)
        cmd, args = args[0], args[1:]
        if cmd == "exit":
            if args and args[0] == "0":
                break
        elif cmd == "echo":
            handle_echo(args)
        elif cmd == "type":
            handle_type(args)
        elif cmd == "pwd":
            print(cur_dir)
        elif cmd == "cd":
            cur_dir = cd_cmd(args, cur_dir)
        else:
            full_path = present_on_path(cmd)
            if full_path:
                res = subprocess.run(args=([cmd] + args), capture_output=True)
                print(res.stdout.decode().rstrip())
                continue
            print(f"{user_input}: command not found")

if __name__ == "__main__":
    main()