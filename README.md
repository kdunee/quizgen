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

- Python 3.10 or later installed.
- An OpenAI API key (available from [OpenAI](https://platform.openai.com/signup)).
- Anki with AnkiConnect installed if you plan to use the Anki import feature.

### PyPI Installation

The easiest way to install QuizGen is via pip:

```bash
pip install quizgen-ai
```

### Development Setup

If you want to contribute or modify the tool, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/kdunee/quizgen.git
   cd quizgen
   ```

1. Install Poetry (if not already installed):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

1. Install the project dependencies:

   ```bash
   poetry install
   ```

1. Set up your OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

### Troubleshooting

- **Python version issues**: Ensure your Python version is 3.10+ by running `python --version`.
- **Poetry installation**: If you encounter issues with Poetry, refer to the [official Poetry documentation](https://python-poetry.org/docs/).
- For additional help, check the [OpenAI documentation](https://platform.openai.com/docs).

## Workflow

Here's the typical workflow for using QuizGen:

1. **Generate Questions:** Use the `generate` command to create questions from your source material. This outputs JSON files.
2. **Convert to CSV (Optional):** If needed, use the `convert` command to convert the JSON files to CSV.
3. **Generate Embeddings:** Use the `embeddings` command to create embeddings from the JSON questions. This is necessary for the next step.
4. **Thin Out Questions (Optional):** Use the `thin` command with the CSV and embeddings to reduce similar questions.
5. **Import to Anki (Optional):** Use the `anki` command with the CSV files to import your questions into Anki.

## Usage

QuizGen provides a unified command-line interface (CLI) to access all its functionalities. Here's how you can use it:

```bash
quizgen <command> [options]
```

**Available Commands:**

- **generate:** Generate questions from educational content.

   ```bash
    # Generate questions from a single chapter:
    quizgen generate --chapter-path path/to/chapter.md --title "Course Title" --output path/to/output.json

    # Generate questions in batch mode:
    quizgen generate --batch --input-dir path/to/source/files --output-dir path/to/output/json --title "Course Title"
    ```

- **convert:** Convert questions from JSON to CSV format.

    ```bash
    # Convert questions to CSV:
    quizgen convert --batch --input-dir path/to/json/files --output-dir path/to/csv/output
    ```

- **embeddings:** Generate embeddings for question comparison.

    ```bash
    # Generate embeddings:
    quizgen embeddings --batch --input-dir path/to/json/files --output-dir path/to/embeddings/output
    ```

- **thin:** Reduce similar questions using embeddings.

    ```bash
    # Thin out questions:
    quizgen thin --csv-dir path/to/csv/files --embeddings-dir path/to/embeddings --output-dir path/to/output --T 10 
    ```

- **anki:** Import questions into Anki.

    ```bash
    # Import to Anki:
    quizgen anki --input-dir path/to/csv/files --root-deck-name "Root Deck Name" 
    ```

## Example Anki Deck

Check out this example Anki deck generated using QuizGen:

- **Gradle Flashcards:** This deck is based on the official Gradle User Manual (October 2024) and covers a wide range of topics related to the Gradle build tool.
  - [Download the Anki deck](https://ankiweb.net/shared/info/1572773429)

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository.
1. Create a new branch (`git checkout -b feature-branch`).
1. Install the project using Poetry: `poetry install`
1. Make your changes.
1. Submit a Pull Request with a description of your changes.

For bug reports or feature requests, please open an issue on GitHub. Ensure that your contributions follow the coding guidelines.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
