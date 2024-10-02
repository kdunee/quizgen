import argparse
import pathlib
import subprocess
from tqdm import tqdm
import sys

def generate_questions(base_dir, title, file_filter, concept_model, questions_model):
    base_dir = pathlib.Path(base_dir).resolve()
    sources_dir = base_dir / 'sources'
    chapters = list(sources_dir.rglob(file_filter))

    for chapter in tqdm(chapters, desc="Generating questions"):
        relative_path = chapter.relative_to(sources_dir)
        output_path = base_dir / 'questions_json' / relative_path.with_suffix('.json')

        # Ensure the output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Skip processing if the output file already exists
        if output_path.exists():
            print(f"Skipping existing chapter: {relative_path}")
            continue

        print(f"Processing chapter: {relative_path}")
        subprocess.run([
            sys.executable, 'generate_questions.py',
            '--title', title,
            '--chapter-path', str(chapter),
            '--output', str(output_path),
            '--concept-model', concept_model,
            '--questions-model', questions_model
        ], check=True)
        print(f"Finished processing chapter: {relative_path}")

    print("Finished processing all chapters")

def main():
    parser = argparse.ArgumentParser(description="Generate questions for multiple chapters")
    parser.add_argument("base_dir", help="Base directory containing sources and questions_json directories")
    parser.add_argument("--title", default="Java Multithreading, Concurrency & Performance Optimization", help="Title of the course")
    parser.add_argument("--filter", default="*.md", help="File filter for source files")
    parser.add_argument("--concept-model", default="gpt-4o-mini-2024-07-18", help="Model to use for concept extraction")
    parser.add_argument("--questions-model", default="gpt-4o-2024-08-06", help="Model to use for question generation")
    args = parser.parse_args()

    generate_questions(args.base_dir, args.title, args.filter, args.concept_model, args.questions_model)

if __name__ == "__main__":
    main()