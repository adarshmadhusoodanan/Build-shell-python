import os
import sys
import subprocess as sbp
from pathlib import Path

PATH = os.environ.get("PATH")

def is_exe(exe_name):
    if PATH:
        for path in PATH.split(":"):
            if Path(path).is_dir():
                for p in Path(path).iterdir():
                    if p.parts[-1] == exe_name.strip():
                        return (True, p)
    return (False, None)

def custom_string_split(string):
    strings = []
    buffer = []
    i = 0
    n = len(string)
    while i < n:
        if string[i] == "\\":
            if i < n:
                i += 1
                buffer.append(string[i])
        elif string[i] == "'":
            temp = i
            i += 1
            while i < n and string[i] != "'":
                i += 1
            if i == n:
                i = temp
                buffer.append(string[i])
            else:
                buffer.extend(string[temp + 1 : i])
        elif string[i] == '"':
            temp = i
            i += 1
            while i < n:
                if string[i] == "\\":
                    if string[i + 1] == '"':
                        i += 2
                        continue
                    elif string[i + 1] == "\\":
                        i += 2
                        continue
                elif string[i] == '"':
                    break
                i += 1
            if i == n:
                i = temp
                buffer.append(string[i])
            else:
                buffer.extend(
                    string[temp + 1 : i]
                    .replace(r"\\n", r"\n")
                    .replace(r'\"', r'"')
                    .replace("\\\\", "\\")
                )
        elif string[i] == " ":
            strings.append("".join(buffer))
            buffer = []
        else:
            buffer.append(string[i])
        i += 1
    if buffer:
        strings.append("".join(buffer))
        buffer = []
    return list(filter(len, strings))

def pwd():
    return os.getcwd()

def change_dir(path):
    if path == "~":
        path = os.environ["HOME"]
    os.chdir(path)

def main():
    builtin_commands = ["exit", "echo", "type", "pwd"]
    while True:
        sys.stdout.write("$ ")
        inp = input()
        command = inp
        argument_string = ""
        argument_vec = []
        splitted_inp = custom_string_split(inp)
        redirect_fd = "1"
        redirect_file = ""

        if len(splitted_inp) > 0:
            command = splitted_inp[0]

        if len(splitted_inp) > 1:
            for i, x in enumerate(splitted_inp[1:]):
                if x == ">":
                    if argument_vec and argument_vec[-1] in ("1", "2"):
                        redirect_fd = argument_vec.pop()
                    redirect_file = splitted_inp[i + 2]
                    break
                elif x == "1>":
                    redirect_file = splitted_inp[i + 2]
                    break
                elif x == "2>":
                    redirect_fd = "2"
                    redirect_file = splitted_inp[i + 2]
                    break
                else:
                    argument_vec.append(x)
            argument_string = " ".join(argument_vec)

        if command == "exit":
            exit_code = int(argument_string.strip()) if argument_string.strip() else 0
            sys.exit(exit_code)

        elif command == "echo":
            output = " ".join(argument_vec) + "\n"
            error = ""

            if redirect_file and redirect_fd == "1":
                with open(redirect_file, "wb") as f:
                    f.write(output.encode())
            else:
                sys.stdout.write(output)

            if redirect_file and redirect_fd == "2":
                with open(redirect_file, "wb") as f:
                    f.write(error.encode())
            else:
                sys.stderr.write(error)

        elif command == "type":
            if argument_string in builtin_commands:
                print(argument_string, "is a shell builtin")
            else:
                ret, exe_dir = is_exe(argument_string)
                if ret:
                    print(f"{argument_string} is {exe_dir}")
                else:
                    print(f"{argument_string}: not found")

        elif command == "pwd":
            print(pwd())

        elif command == "cd":
            path = argument_string
            if path == "~":
                path = os.environ["HOME"]
            if Path(path).exists():
                change_dir(path)
            else:
                print(f"cd: {path}: No such file or directory")

        else:
            ret, exe_dir = is_exe(command)
            if ret:
                arguments_list = [command]
                if argument_vec:
                    arguments_list.extend(argument_vec)

                capture_output = True if redirect_file else False

                cmp_process = sbp.run(
                    arguments_list, shell=False, capture_output=capture_output
                )

                if redirect_file:
                    if redirect_fd == "1":
                        if cmp_process.stderr:
                            sys.stderr.write(cmp_process.stderr.decode())
                        with open(redirect_file, "wb") as f:
                            f.write(cmp_process.stdout)
                    elif redirect_fd == "2":
                        if cmp_process.stdout:
                            sys.stdout.write(cmp_process.stdout.decode())
                        with open(redirect_file, "wb") as f:
                            f.write(cmp_process.stderr)
            else:
                print(f"{inp}: command not found")

if __name__ == "__main__":
    main()
