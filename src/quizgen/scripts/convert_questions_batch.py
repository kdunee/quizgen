import argparse
import pathlib
import subprocess
import sys
import os

from tqdm import tqdm


def convert_questions(input_dir, output_dir):
    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    json_files = list(input_dir.rglob("*.json"))

    for json_file in tqdm(json_files, desc="Converting files"):
        relative_path = json_file.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix(".csv")

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing file: {relative_path}")
            continue

        print(f"Processing file: {relative_path}")
        script_path = os.path.join(os.path.dirname(__file__), "convert_questions.py")
        subprocess.run(
            [sys.executable, script_path, str(json_file), str(output_path)],
            check=True,
        )
        print(f"Finished processing file: {relative_path}")

    print("Finished processing all files")


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON question files to CSV format"
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Input directory containing JSON question files",
    )
    parser.add_argument(
        "--output-dir", required=True, help="Output directory for CSV files"
    )
    args = parser.parse_args()

    convert_questions(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
