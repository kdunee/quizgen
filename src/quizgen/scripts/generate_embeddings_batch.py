import argparse
import pathlib
import subprocess
import sys
import os

from tqdm import tqdm


def generate_embeddings(input_dir, output_dir, embedding_model):
    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    json_files = list(input_dir.rglob("*.json"))

    for json_file in tqdm(json_files, desc="Generating embeddings"):
        relative_path = json_file.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix(".npy")

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing file: {relative_path}")
            continue

        print(f"Processing file: {relative_path}")
        script_path = os.path.join(os.path.dirname(__file__), "generate_embeddings.py")
        subprocess.run(
            [
                sys.executable,
                script_path,
                "--input-path",
                str(json_file),
                "--output-path",
                str(output_path),
                "--embedding-model",
                embedding_model,
            ],
            check=True,
        )
        print(f"Finished processing file: {relative_path}")

    print("Finished processing all files")


def main():
    parser = argparse.ArgumentParser(
        description="Generate embeddings for JSON question files"
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Input directory containing JSON question files",
    )
    parser.add_argument(
        "--output-dir", required=True, help="Output directory for embedding files"
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default="text-embedding-3-small",
        help="Model to use for generating embeddings",
    )
    args = parser.parse_args()

    generate_embeddings(args.input_dir, args.output_dir, args.embedding_model)


if __name__ == "__main__":
    main()
