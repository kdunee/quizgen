import json
import csv
import argparse


def json_to_anki_csv(input_file, output_file):
    """
    Converts a JSON file containing questions and answers to a CSV file suitable for Anki import.

    Args:
      input_file: Path to the input JSON file.
      output_file: Path to the output CSV file.
    """

    with open(input_file, "r") as f:
        data = json.load(f)

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        for item in data:
            question = item["question"]
            options = item["options"]
            options_text = "<br>".join(
                [f"{key}. {value}" for key, value in options.items()]
            )
            front = f"{question}<br><br>{options_text}"

            correct_answer = item["correct_answer"]
            explanation = item["explanation"]
            back = f"<b>Correct Answer:</b> {correct_answer}<br><br>{explanation}"

            writer.writerow([front, back])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert JSON questions to Anki CSV format."
    )
    parser.add_argument(
        "--input-path", required=True, help="Path to the input JSON file."
    )
    parser.add_argument(
        "--output-path", required=True, help="Path to the output CSV file."
    )
    args = parser.parse_args()

    json_to_anki_csv(args.input_path, args.output_path)
    print(f"CSV file created at: {args.output_path}")
