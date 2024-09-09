import subprocess

VENV_PATH = "../venv1"

def run_command(command):
    """Запускает команду в shell и выводит результат."""
    try:
        print(f"Запуск команды: {command}")
        # Включаем активацию venv перед выполнением команды
        result = subprocess.run(
            f"source {VENV_PATH}/bin/activate && {command}",
            shell=True, check=True, text=True, capture_output=True, executable="/bin/bash"
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
        print(e.stderr)

def main():
    # run_command(f"python3 -m venv {VENV_PATH}")
    #
    # run_command("pip install -r ../requirements.txt")
    #
    # run_command("python pars_groups.py")
    # run_command("python pars_lessons_time.py")
    # run_command("python pars_teachers_data.py")

    run_command("cd ../server && python manage.py makemigrations")
    run_command("cd ../server && python manage.py migrate")
    run_command("cd ../server && python manage.py loaddata data/teachers_db_data.json")
    print("Все команды и скрипты выполнены успешно!")

if __name__ == "__main__":
    main()
