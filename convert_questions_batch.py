import argparse
import pathlib
import subprocess
from tqdm import tqdm
import sys

def convert_questions(base_dir):
    base_dir = pathlib.Path(base_dir).resolve()
    questions_dir = base_dir / 'questions_json'
    json_files = list(questions_dir.rglob('*.json'))

    for json_file in tqdm(json_files, desc="Converting files"):
        relative_path = json_file.relative_to(questions_dir)
        output_path = base_dir / 'questions_csv' / relative_path.with_suffix('.csv')

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing file: {relative_path}")
            continue

        print(f"Processing file: {relative_path}")
        subprocess.run([sys.executable, 'convert_questions.py', str(json_file), str(output_path)], check=True)
        print(f"Finished processing file: {relative_path}")

    print("Finished processing all files")

def main():
    parser = argparse.ArgumentParser(description="Convert JSON question files to CSV format")
    parser.add_argument("base_dir", help="Base directory containing questions_json and questions_csv directories")
    args = parser.parse_args()

    convert_questions(args.base_dir)

if __name__ == "__main__":
    main()
