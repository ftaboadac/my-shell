import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        commands = ['echo','exit','type']
        parts = command.split()
        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            if len(parts) > 1 and parts[1] in commands:
                print(f"{parts[1]} is a shell builtin")
            else:
                print(f"{parts[1]}: not found")
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
