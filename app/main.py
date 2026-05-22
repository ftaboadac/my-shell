import sys
import os
import subprocess


def main():
    while True:

        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        commands = ['echo','exit','type','pwd','cd']
        parts = parse(command)
        parts, redirect_target, error_mode = parse_redirects(parts)
        path = os.environ['PATH']
        folders = path.split(os.pathsep)
        cwd = os.getcwd()
        home = os.getenv('HOME')

        if redirect_target and not error_mode:
            out = open(redirect_target, 'w')
        else:
            out = None

        if redirect_target and error_mode:
            out_err = open(redirect_target, 'w')
        else:
            out_err = None

        if command == "exit":
            break

        elif command.startswith("echo"):
            print(" ".join(parts[1:]), file=out)

        elif command == "pwd":
            print(cwd, file=out)

        elif command.startswith("cd"):
            cd_path = parts[1]
            if cd_path == '~':
                os.chdir(home)
            elif os.path.isdir(cd_path):
                os.chdir(cd_path)
            else:
                print(f"cd: {cd_path}: No such file or directory", file=out_err)

        elif command.startswith("type"):
            if len(parts) > 1 and parts[1] in commands:
                print(f"{parts[1]} is a shell builtin")
            else:
                found = False
                for folder in folders:
                    if os.path.isdir(folder):
                        path_to_file = os.path.join(folder,parts[1])
                        if os.path.exists(path_to_file) and os.access(path_to_file, os.X_OK):
                            print(f"{parts[1]} is {path_to_file}")
                            found = True
                            break
                if not found:
                  print(f"{parts[1]}: not found", file=out_err)
               
        elif parts[0] not in commands:
            path_to_file = is_exec(parts[0], folders)

            if path_to_file:
                result = subprocess.run([parts[0]] + parts[1:],text=True, stdout=out, stderr=out_err)
            else:
                print(f"{command}: command not found")

        if out:
            out.close()

def is_exec(part, folders):
    for folder in folders:
        if os.path.isdir(folder):
            path_to_file = os.path.join(folder,part)
            if os.path.exists(path_to_file) and os.access(path_to_file, os.X_OK):
                return path_to_file
    return None

def parse(line):
    tokens = []
    current = ""
    in_single = False
    in_double = False
    escape_next = False

    for char in line:

        if escape_next:
            current += char
            escape_next = False
        elif char == "'" and not in_single and not in_double:
            in_single = True
        elif char == '"' and not in_double and not in_single:
            in_double = True            
        elif char == "'" and in_single:
            in_single = False
        elif char == '"' and in_double:
            in_double = False   
        elif char == "\\" and not in_single: 
            escape_next = True  
        elif char == " " and not in_single and not in_double:
            if current:
                tokens.append(current)
                current = ""
        else:
            current += char

    if current:
        tokens.append(current)    
    return tokens


def parse_redirects(tokens):
    error_mode = False

    if '>' in tokens:
        index = tokens.index('>')

        before = tokens[:index]
        after = tokens[index + 1:]

        return before, after[0], error_mode

    if '1>' in tokens:
        index = tokens.index('1>')

        before = tokens[:index]
        after = tokens[index + 1:]

        return before, after[0], error_mode

    if '2>' in tokens:
        index = tokens.index('2>')

        before = tokens[:index]
        after = tokens[index + 1:]
        error_mode = True

        return before, after[0], error_mode

    else:
        return tokens, None, error_mode



if __name__ == "__main__":
    main()
