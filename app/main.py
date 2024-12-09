import sys


def main():
    # Uncomment this block to pass the first stage


    valid_commands = []

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        # Wait for user input
        user_command = input()
        if user_command not in valid_commands:
            print(f"{user_command}: command not found")
            continue

if __name__ == "__main__":
    main()
