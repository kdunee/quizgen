import argparse
import pathlib
import subprocess
from tqdm import tqdm
import sys

def generate_embeddings(base_dir):
    base_dir = pathlib.Path(base_dir).resolve()
    questions_dir = base_dir / 'questions_json'
    json_files = list(questions_dir.rglob('*.json'))

    for json_file in tqdm(json_files, desc="Generating embeddings"):
        relative_path = json_file.relative_to(questions_dir)
        output_path = base_dir / 'questions_embeddings' / relative_path.with_suffix('.npy')

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing file: {relative_path}")
            continue

        print(f"Processing file: {relative_path}")
        subprocess.run([sys.executable, 'generate_embeddings.py', '--input-path', str(json_file), '--output-path', str(output_path)], check=True)
        print(f"Finished processing file: {relative_path}")

    print("Finished processing all files")

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for JSON question files")
    parser.add_argument("base_dir", help="Base directory containing questions_json and questions_embeddings directories")
    args = parser.parse_args()

    generate_embeddings(args.base_dir)

if __name__ == "__main__":
    main()