import sys
import os
import subprocess

def mysplit(input):
    res = [""]
    current_quote = ""
    i = 0
    while i < len(input):
        c = input[i]
        if c == "\\":
            ch = input[i + 1]
            if current_quote == "'":
                res[-1] += c
            elif current_quote == '"':
                ch = input[i + 1]
                if ch in ["\\", "$", '"', "\n"]:
                    res[-1] += ch
                else:
                    res[-1] += "\\" + ch
                i += 1
            else:
                res[-1] += input[i + 1]
                i += 1
        elif c in ['"', "'"]:
            if current_quote == "":
                current_quote = c
            elif current_quote == c:
                current_quote = ""
            else:
                res[-1] += c
        elif c == " " and current_quote == "":
            if res[-1] != "":
                res.append("")
        else:
            res[-1] += c
        i += 1
    if res[-1] == "":
        res.pop()
    return res

def get_user_command():
    sys.stdout.write("$ ")
    out, err = sys.stdout, sys.stderr
    inp = mysplit(input())
    if "1>" in inp:
        idx = inp.index("1>")
        inp, out = inp[:idx], inp[idx + 1]
    elif ">" in inp:
        idx = inp.index(">")
        inp, out = inp[:idx], inp[idx + 1]
    return inp, out, err

def get_file(dirs, filename):
    for dir in dirs:
        filepath = f"{dir}/{filename}"
        if os.path.isfile(filepath):
            return filepath
    return None

def handle_command(inp, dirs, HOME, out, err):
    toCloseOut = False
    if type(out) is str:
        toCloseOut = True
        out = open(out, "w+")
    if len(inp) == 2 and inp[0] == "exit" and inp[1] == "0":
        sys.exit(0)
    elif inp[0] == "echo":
        out.write(" ".join(inp[1:]) + "\n")
    elif len(inp) == 2 and inp[0] == "type":
        arg = inp[1]
        if arg in ["type", "exit", "echo", "pwd", "cd"]:
            out.write(f"{arg} is a shell builtin\n")
        else:
            filepath = get_file(dirs, arg)
            if filepath:
                out.write(f"{arg} is {filepath}\n")
            else:
                out.write(f"{arg}: not found\n")
    elif inp[0] == "pwd":
        out.write(f"{os.getcwd()}\n")
    elif len(inp) == 2 and inp[0] == "cd":
        path = inp[1]
        if path == "~":
            os.chdir(HOME)
        elif os.path.isdir(path):
            os.chdir(path)
        else:
            err.write(f"cd: {path}: No such file or directory\n")
    else:
        file = inp[0]
        filepath = get_file(dirs, file)
        if filepath:
            subprocess.run([filepath, *inp[1:]], stdout=out, stderr=err)
        else:
            err.write(f"{' '.join(inp)}: command not found\n")
    if toCloseOut:
        out.close()

def main(dirs, HOME):
    while True:
        inp, out, err = get_user_command()
        handle_command(inp, dirs, HOME, out, err)

if __name__ == "__main__":
    PATH = os.environ.get("PATH")
    dirs = PATH.split(":")
    HOME = os.environ.get("HOME")
    main(dirs, HOME)
