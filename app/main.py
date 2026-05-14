import sys
import os
import subprocess


def main():
    while True:

        sys.stdout.write("$ ")
        sys.stdout.flush()
        command = input()
        commands = ['echo','exit','type','pwd','cd']
        parts = command.split()
        path = os.environ['PATH']
        folders = path.split(os.pathsep)
        cwd = os.getcwd()
        home = os.getenv('HOME')

        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command == "pwd":
            print(cwd)
        elif command.startswith("cd"):
            cd_path = parts[1]
            if cd_path == '~':
                os.chdir(home)
            if os.path.isdir(cd_path):
                os.chdir(cd_path)
            else:
                print(f"cd: {cd_path}: No such file or directory")
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
                  print(f"{parts[1]}: not found")
        elif parts[0] not in commands:
            path_to_file = is_exec(parts[0], folders)

            if path_to_file:
                result = subprocess.run([parts[0]] + parts[1:],capture_output=True,text=True)
                print(result.stdout, end="")
            else:
                print(f"{command}: command not found")


def is_exec(part, folders):
    for folder in folders:
        if os.path.isdir(folder):
            path_to_file = os.path.join(folder,part)
            if os.path.exists(path_to_file) and os.access(path_to_file, os.X_OK):
                return path_to_file
    return None

if __name__ == "__main__":
    main()
