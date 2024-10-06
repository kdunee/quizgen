import argparse
import subprocess
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Question Generation Tool")
    subparsers = parser.add_subparsers(dest='command')

    # Generate Questions
    generate_parser = subparsers.add_parser('generate', help='Generate questions from educational content')
    generate_parser.add_argument('--chapter-path', help='Path to the chapter file')
    generate_parser.add_argument('--title', help='Title of the course/chapter')
    generate_parser.add_argument('--output', help='Path to the output JSON file')
    generate_parser.add_argument('--batch', action='store_true', help='Process multiple chapters in batch mode')
    generate_parser.add_argument('--input-dir', help='Path to the directory containing source files (batch mode)')
    generate_parser.add_argument('--output-dir', help='Path to the output directory for JSON files (batch mode)')
    generate_parser.add_argument('--file-filter', default="*.md", help='File filter for batch processing (e.g., "*.md")')

    # Convert Questions
    convert_parser = subparsers.add_parser('convert', help='Convert questions from JSON to CSV format')
    convert_parser.add_argument('--input-path', help='Path to the input JSON file')
    convert_parser.add_argument('--output-path', help='Path to the output CSV file')
    convert_parser.add_argument('--batch', action='store_true', help='Convert multiple JSON files in batch mode')
    convert_parser.add_argument('--input-dir', help='Path to the directory containing JSON files (batch mode)')
    convert_parser.add_argument('--output-dir', help='Path to the output directory for CSV files (batch mode)')

    # Generate Embeddings
    embeddings_parser = subparsers.add_parser('embeddings', help='Generate embeddings for question comparison')
    embeddings_parser.add_argument('--input-path', help='Path to the input JSON file')
    embeddings_parser.add_argument('--output-path', help='Path to the output embeddings file')
    embeddings_parser.add_argument('--batch', action='store_true', help='Generate embeddings for multiple files in batch mode')
    embeddings_parser.add_argument('--input-dir', help='Path to the directory containing JSON files (batch mode)')
    embeddings_parser.add_argument('--output-dir', help='Path to the output directory for embeddings files (batch mode)')

    # Thin Out Questions
    thin_parser = subparsers.add_parser('thin', help='Reduce similar questions using embeddings')
    thin_parser.add_argument('--csv-dir', help='Path to the directory containing CSV files')
    thin_parser.add_argument('--embeddings-dir', help='Path to the directory containing embeddings')
    thin_parser.add_argument('--output-dir', help='Path to the output directory')
    thin_parser.add_argument('--T', type=int, help='Target number of questions to retain')

    # Import to Anki
    anki_parser = subparsers.add_parser('anki', help='Import questions into Anki')
    anki_parser.add_argument('--input-dir', help='Path to the directory containing CSV files')
    anki_parser.add_argument('--root-deck-name', help='Name of the root deck in Anki')

    args = parser.parse_args()

    script_dir = os.path.join(os.path.dirname(__file__), 'scripts')

    if args.command == 'generate':
        if args.batch:
            script_path = os.path.join(script_dir, 'generate_questions_batch.py')
        else:
            script_path = os.path.join(script_dir, 'generate_questions.py')
    elif args.command == 'convert':
        if args.batch:
            script_path = os.path.join(script_dir, 'convert_questions_batch.py')
        else:
            script_path = os.path.join(script_dir, 'convert_questions.py')
    elif args.command == 'embeddings':
        if args.batch:
            script_path = os.path.join(script_dir, 'generate_embeddings_batch.py')
        else:
            script_path = os.path.join(script_dir, 'generate_embeddings.py')
    elif args.command == 'thin':
        script_path = os.path.join(script_dir, 'thin_out_questions.py')
    elif args.command == 'anki':
        script_path = os.path.join(script_dir, 'import_to_anki.py')
    else:
        parser.print_help()
        return

    # Construct the command
    cmd = [sys.executable, script_path]
    for arg, value in vars(args).items():
        if value is not None and arg != 'command' and arg != 'batch':  # Exclude command and batch
            cmd.extend([f'--{arg.replace("_", "-")}', str(value)])

    # Execute the subprocess
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
