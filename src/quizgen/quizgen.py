import subprocess
import sys
import os


def print_help():
    print(
        "Please provide a command. Available commands: generate, convert, embeddings, thin, anki"
    )
    print("\nUsage:")
    print("  quizgen <command> [--batch] [subscript arguments]")
    print("\nCommands:")
    print("  generate     Generate questions from educational content")
    print("  convert      Convert questions from JSON to CSV format")
    print("  embeddings  Generate embeddings for question comparison")
    print("  thin         Reduce similar questions using embeddings")
    print("  anki        Import questions into Anki")
    print("\nOptions:")
    print(
        "  --batch      Enable batch processing mode for supported commands (generate, convert, embeddings)"
    )


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1]
    script_dir = os.path.join(os.path.dirname(__file__), "scripts")

    if command == "generate":
        script_path = (
            os.path.join(script_dir, "generate_questions_batch.py")
            if "--batch" in sys.argv
            else os.path.join(script_dir, "generate_questions.py")
        )
    elif command == "convert":
        script_path = (
            os.path.join(script_dir, "convert_questions_batch.py")
            if "--batch" in sys.argv
            else os.path.join(script_dir, "convert_questions.py")
        )
    elif command == "embeddings":
        script_path = (
            os.path.join(script_dir, "generate_embeddings_batch.py")
            if "--batch" in sys.argv
            else os.path.join(script_dir, "generate_embeddings.py")
        )
    elif command == "thin":
        script_path = os.path.join(script_dir, "thin_out_questions.py")
    elif command == "anki":
        script_path = os.path.join(script_dir, "import_to_anki.py")
    else:
        print_help()
        return

    # Construct the command with ALL arguments, except --batch
    cmd = [sys.executable, script_path] + [
        arg for arg in sys.argv[2:] if arg != "--batch"
    ]

    # Execute the subprocess
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
