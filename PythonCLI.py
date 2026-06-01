import sys
import os
import subprocess
import shutil
import webbrowser
from urllib.parse import urlparse

def main():
    print(" ------- PythonCLI ------- ")
    print("Type 'help' for a list of commands, or 'exit' to quit.")


def run_system_command(command, shell=False):
    try:
        completed = subprocess.run(command, shell=shell)
        if completed.returncode != 0:
            print(f"Command failed with exit code {completed.returncode}")
            return False
        return True
    except FileNotFoundError:
        print("Command not found.")
    except Exception as e:
        print(f"Error running command: {e}")
    return False


def install_git():
    if shutil.which("git"):
        print("Git is already installed.")
        return
    print("Installing Git...")
    if os.name == 'nt':
        if shutil.which('winget'):
            run_system_command(['winget', 'install', '--id', 'Git.Git', '-e', '--source', 'winget'])
        else:
            print("Winget is not available on this system. Please install Git manually from https://git-scm.com/downloads")
            return
    elif sys.platform == 'darwin':
        if shutil.which('brew'):
            run_system_command(['brew', 'install', 'git'])
        else:
            print("Homebrew is not installed. Please install Homebrew first or install Git manually.")
            return
    else:
        if shutil.which('apt-get'):
            run_system_command(['sudo', 'apt-get', 'update'])
            run_system_command(['sudo', 'apt-get', 'install', '-y', 'git'])
        elif shutil.which('yum'):
            run_system_command(['sudo', 'yum', 'install', '-y', 'git'])
        elif shutil.which('dnf'):
            run_system_command(['sudo', 'dnf', 'install', '-y', 'git'])
        else:
            print("No supported package manager found. Please install Git manually.")
            return
    if shutil.which('git'):
        print("Git installed successfully.")
    else:
        print("Git installation may have failed. Please check the output above.")


def uninstall_git():
    if not shutil.which('git'):
        print("Git is not installed.")
        return
    print("Uninstalling Git...")
    if os.name == 'nt':
        if shutil.which('winget'):
            run_system_command(['winget', 'uninstall', '--id', 'Git.Git', '-e'])
        else:
            print("Winget is not available on this system. Please uninstall Git manually from Control Panel or Settings.")
            return
    elif sys.platform == 'darwin':
        if shutil.which('brew'):
            run_system_command(['brew', 'uninstall', 'git'])
        else:
            print("Homebrew is not installed. Please remove Git manually if needed.")
            return
    else:
        if shutil.which('apt-get'):
            run_system_command(['sudo', 'apt-get', 'remove', '-y', 'git'])
        elif shutil.which('yum'):
            run_system_command(['sudo', 'yum', 'remove', '-y', 'git'])
        elif shutil.which('dnf'):
            run_system_command(['sudo', 'dnf', 'remove', '-y', 'git'])
        else:
            print("No supported package manager found. Please uninstall Git manually.")
            return
    if not shutil.which('git'):
        print("Git uninstalled successfully.")
    else:
        print("Git uninstall may have failed. Please check the output above.")

while True:
    main()
    command = input(">>> ").strip().lower()
    if command == 'help':
        print("Available commands:")
        print("  help - Show this help message")
        print("  exit - Exit the CLI")
        print("  youtube - Open a YouTube video in your default browser")
        print("  run - Run or open a file (any type)")
        print("  quiz - Take a short interactive quiz")
        print("  echo - Echo a message")
        print("  info - Show program information")
        print("  git install - Install Git on this machine")
        print("  git uninstall - Uninstall Git from this machine")
    elif command == 'exit':
        print("Exiting PythonCLI. Goodbye!")
        sys.exit(0)
    elif command == 'youtube':
        input_url = input("Enter a YouTube URL: ").strip()
        parsed_url = urlparse(input_url)
        if parsed_url.netloc in ['www.youtube.com', 'youtube.com', 'youtu.be']:
            webbrowser.open(input_url)
            print("Opening YouTube video in your default browser...")
        else:
            print("Invalid YouTube URL. Please try again.")
    elif command == 'run':
        file_to_run = input("Enter path to file to run/open: ").strip()
        if not os.path.isfile(file_to_run):
            print("File not found. Please check the path and try again.")
        else:
            ext = os.path.splitext(file_to_run)[1].lower()
            try:
                if ext == '.py':
                    print(f"Running {file_to_run} with {sys.executable}...")
                    completed = subprocess.run([sys.executable, file_to_run])
                    if completed.returncode != 0:
                        print(f"Process exited with code {completed.returncode}")
                else:
                    # Non-Python files: open with default application or execute on supported platforms
                    if os.name == 'nt':
                        # On Windows, prefer os.startfile to open with associated app
                        try:
                            print(f"Opening {file_to_run} with the default application...")
                            os.startfile(file_to_run)
                        except OSError:
                            # Fall back to subprocess for executables
                            completed = subprocess.run([file_to_run], shell=True)
                            if completed.returncode != 0:
                                print(f"Process exited with code {completed.returncode}")
                    elif sys.platform == 'darwin':
                        print(f"Opening {file_to_run} with the default application...")
                        completed = subprocess.run(['open', file_to_run])
                        if completed.returncode != 0:
                            print(f"Process exited with code {completed.returncode}")
                    else:
                        print(f"Opening {file_to_run} with the default application...")
                        completed = subprocess.run(['xdg-open', file_to_run])
                        if completed.returncode != 0:
                            print(f"Process exited with code {completed.returncode}")
            except Exception as e:
                print(f"Error running/opening file: {e}")
    elif command == 'quiz':
        questions = [
            ("What is the capital of France?", "paris"),
            ("What is 2+2?", "4"),
            ("Which language is this program written in?", "python"),
        ]
        score = 0
        print("Starting quiz. Type your answer and press Enter.")
        for q, a in questions:
            ans = input(q + " ").strip().lower()
            if ans == a:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer is: {a}")
        print(f"Quiz finished. Score: {score}/{len(questions)}")
    elif command == 'echo':
        message = input("Enter a message to echo: ")
        print(f"Echo: {message}")
    elif command == 'info':
        print("PythonCLI version 1.01 beta - A simple command-line interface built with Python.")
    elif command == 'git install':
        install_git()
    elif command == 'git uninstall':
        uninstall_git()
    else:
        print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")