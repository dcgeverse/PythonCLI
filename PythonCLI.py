import sys
import os
import subprocess
import webbrowser
from urllib.parse import urlparse

def main():
    print(" ------- PythonCLI ------- ")
    print("Type 'help' for a list of commands, or 'exit' to quit.")

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
    else:
        print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")