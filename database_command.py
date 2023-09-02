import subprocess


def run_preset_command(command_number):
    if command_number == 1:
        preset_command = "flask db init"
    elif command_number == 2:
        preset_command = "flask db migrate -m 'migrate'"
    elif command_number == 3:
        preset_command = "flask db upgrade"
    elif command_number == 4:
        preset_command = "flask run --host=0.0.0.0 --port=5000"
    else:
        print("Invalid command number")
        return

    result = subprocess.run(
        preset_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Error executing command:")
        print(result.stderr)


command_number = int(
    input("Select a command number\n1: init\n2: migrate\n3: upgrade\n4: run flask\n->")
)
run_preset_command(command_number)
