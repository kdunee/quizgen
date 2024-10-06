# QuizGen: AI-Powered Question Generation Tool

*Effortlessly create AI-generated quizzes from your educational content.*

QuizGen is a Python-based tool that generates quiz questions from educational materials using state-of-the-art AI models. It's designed for educators, course creators, and developers looking to automate question creation from textbooks, lecture notes, and other learning resources, saving time and enhancing the learning experience. With QuizGen, you can streamline quiz creation for online courses, exam preparation, and interactive learning tools like Anki.

The tool processes content, extracts key concepts, generates relevant questions, and outputs them in formats suitable for e-learning platforms, such as Anki.

## Key Features

- **Automatic concept extraction**: Identifies key concepts from provided educational content.
- **AI-powered question generation**: Uses advanced AI models to create high-quality, diverse quiz questions.
- **Question similarity reduction**: Reduces redundancy in generated questions by comparing embeddings.
- **Anki integration**: Easily import generated questions into Anki for flashcard-based learning.
- **Extensible and customizable**: Modify templates and fine-tune the output to suit specific educational needs.

## Installation

Before you begin, ensure you have:

- Python 3.8 or later installed.
- An OpenAI API key (available from [OpenAI](https://platform.openai.com/signup)).

### Step-by-Step Setup

1. Clone the repository:

   ```bash
   git clone [https://github.com/kdunee/quizgen.git](https://github.com/kdunee/quizgen.git)
   cd quizgen
   ```

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

1. Set up your OpenAI API key:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

### Troubleshooting

- **Python version issues**: Ensure your Python version is 3.8+ by running `python --version`.
- **Outdated `pip`**: Upgrade `pip` if needed by running `python -m pip install --upgrade pip`.
- For additional help, check the [OpenAI documentation](https://platform.openai.com/docs).

## Workflow

Here's the typical workflow for using QuizGen:

1. **Generate Questions:** Use `generate_questions.py` or `generate_questions_batch.py` to create questions from your source material. This outputs JSON files.
2. **Convert to CSV (Optional):** If needed, use `convert_questions.py` or `convert_questions_batch.py` to convert the JSON files to CSV.
3. **Generate Embeddings:** Use `generate_embeddings.py` or `generate_embeddings_batch.py` to create embeddings from the JSON questions. This is necessary for the next step.
4. **Thin Out Questions (Optional):**  Use `thin_out_questions.py` with the CSV and embeddings to reduce similar questions.
5. **Import to Anki (Optional):** Use `import_to_anki.py` with the CSV files to import your questions into Anki.

## Usage

This section outlines the steps for using QuizGen. Note that some steps depend on the output of previous steps.

### Generating Questions

To generate questions from your educational content (output: JSON files):

```bash
python generate_questions.py --chapter-path path/to/chapter.md --title "Course Title" --output path/to/output.json
```

For batch processing multiple chapters:

```bash
python generate_questions_batch.py --input-dir path/to/source/files --output-dir path/to/output/json --title "Course Title" --file-filter "*.md"
```

### Converting Questions to CSV (Optional)

To convert JSON questions to CSV format for easier review or integration with other tools (requires JSON output from "Generating Questions"):

```bash
python convert_questions_batch.py --input-dir path/to/json/files --output-dir path/to/csv/output
```

Or, for a single file:

```bash
python convert_questions.py --input-path input_file.json --output-path output_file.csv
```

### Generating Embeddings

To create embeddings for generated questions (requires JSON output from "Generating Questions"):

```bash
python generate_embeddings_batch.py --input-dir path/to/json/files --output-dir path/to/embeddings/output
```

Or for a single file:

```bash
python generate_embeddings.py --input-path input_questions.json --output-path output_embeddings.npy
```

### Thinning Out Questions (Optional)

To reduce similar questions based on their embeddings (requires CSV and embeddings output from previous steps):

```bash
python thin_out_questions.py --csv-dir path/to/csv/files --embeddings-dir path/to/embeddings --output-dir path/to/output --T number_of_expected_questions
```

- `--T`: Specifies the target number of questions to retain.

### Importing to Anki (Optional)

To import questions into Anki as flashcards (requires CSV output from "Converting Questions to CSV"):

```bash
python import_to_anki.py --input-dir path/to/csv/files --root-deck-name "Root Deck Name"
```

Ensure Anki is installed and properly set up (with AnkiConnect) before importing.

## Project Structure

- `generate_questions.py`: Core script for generating questions from a single chapter.
- `generate_questions_batch.py`: Processes multiple chapters in batch.
- `convert_questions.py`: Converts generated questions from JSON to CSV format.
- `convert_questions_batch.py`: Batch converts JSON questions to CSV.
- `generate_embeddings.py`: Generates embeddings for question comparison.
- `generate_embeddings_batch.py`: Batch processing of embeddings.
- `thin_out_questions.py`: Reduces similar questions using embeddings.
- `import_to_anki.py`: Imports CSV-formatted questions into Anki.

### Directories

- `prompts/`: Templates used by AI models to guide question generation.
- `examples/`: Sample source materials and example outputs demonstrating usage.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Submit a Pull Request with a description of your changes.

For bug reports or feature requests, please open an issue on GitHub. Ensure that your contributions follow the coding guidelines.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
