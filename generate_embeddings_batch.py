import argparse
import pathlib
import subprocess
from tqdm import tqdm
import sys

def generate_embeddings(input_dir, output_dir):
    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    json_files = list(input_dir.rglob('*.json'))

    for json_file in tqdm(json_files, desc="Generating embeddings"):
        relative_path = json_file.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix('.npy')

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
    parser.add_argument("--input-dir", required=True, help="Input directory containing JSON question files")
    parser.add_argument("--output-dir", required=True, help="Output directory for embedding files")
    args = parser.parse_args()

    generate_embeddings(args.input_dir, args.output_dir)

if __name__ == "__main__":
    main()