import sys
import os

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        commands = ['echo','exit','type']
        parts = command.split()
        path = os.environ['PATH']
        folders = path.split(os.pathsep)

        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            if len(parts) > 1 and parts[1] in commands:
                print(f"{parts[1]} is a shell builtin")
            else:
                for folder in folders:
                    if os.path.isdir(folder):
                        path_to_file = os.path.join(folder,parts[1])
                        if os.path.exists(path_to_file) and os.access(path_to_file, os.X_OK):
                                print(f"{parts[1]} is {path_to_file}")
                                return
                        else:
                            continue
                print(f"{parts[1]}: not found")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
