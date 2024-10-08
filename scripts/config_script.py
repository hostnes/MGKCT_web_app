import subprocess

from conf import VENV_PATH

def run_command(command, is_venv=True):
    """Запускает команду в shell и выводит результат."""
    try:
        print(f"Запуск команды: {command}")
        if is_venv == True:
            result = subprocess.run(
                f"source {VENV_PATH}/bin/activate && {command}",
                shell=True, check=True, text=True, capture_output=True, executable="/bin/bash"
            )
        else:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, executable="/bin/bash")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(e.stderr)


def main():
    run_command(f"python3 -m venv {VENV_PATH}", False)

    run_command("pip install -r ../requirements.txt")

    run_command("python pars_groups.py")
    run_command("python pars_lessons_time.py")
    run_command("python pars_teachers_data.py")

    run_command("cd ../server && python manage.py makemigrations")
    run_command("cd ../server && python manage.py migrate")
    run_command("cd ../server && python manage.py loaddata data/teachers_db_data.json")
    print("Все команды и скрипты выполнены успешно!")

if __name__ == "__main__":
    main()
