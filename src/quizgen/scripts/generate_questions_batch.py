import argparse
import pathlib
import subprocess
import sys
import os

from tqdm import tqdm


def generate_questions(
    input_dir, output_dir, title, file_filter, concept_model, questions_model
):
    input_dir = pathlib.Path(input_dir).resolve()
    output_dir = pathlib.Path(output_dir).resolve()
    chapters = list(input_dir.rglob(file_filter))

    for chapter in tqdm(chapters, desc="Generating questions"):
        relative_path = chapter.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix(".json")

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing chapter: {relative_path}")
            continue

        print(f"Processing chapter: {relative_path}")
        script_path = os.path.join(os.path.dirname(__file__), "generate_questions.py")
        subprocess.run(
            [
                sys.executable,
                script_path,
                "--title",
                title,
                "--chapter-path",
                str(chapter),
                "--output",
                str(output_path),
                "--concept-model",
                concept_model,
                "--questions-model",
                questions_model,
            ],
            check=True,
        )
        print(f"Finished processing chapter: {relative_path}")

    print("Finished processing all chapters")


def main():
    parser = argparse.ArgumentParser(
        description="Generate questions for multiple chapters"
    )
    parser.add_argument(
        "--input-dir", required=True, help="Input directory containing source files"
    )
    parser.add_argument(
        "--output-dir", required=True, help="Output directory for JSON question files"
    )
    parser.add_argument("--title", required=True, help="Title of the course")
    parser.add_argument(
        "--file-filter", default="*.md", help="File filter for source files"
    )
    parser.add_argument(
        "--concept-model",
        default="gpt-4o-mini-2024-07-18",
        help="Model to use for concept extraction",
    )
    parser.add_argument(
        "--questions-model",
        default="gpt-4o-2024-08-06",
        help="Model to use for question generation",
    )
    args = parser.parse_args()

    generate_questions(
        args.input_dir,
        args.output_dir,
        args.title,
        args.file_filter,
        args.concept_model,
        args.questions_model,
    )


if __name__ == "__main__":
    main()
