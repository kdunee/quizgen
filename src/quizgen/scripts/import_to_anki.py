import os
import csv
import json
import urllib.request
import argparse


def request(action, **params):
    return {"action": action, "params": params, "version": 6}


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode("utf-8")
    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request("http://127.0.0.1:8765", requestJson)
        )
    )
    if len(response) != 2:
        raise Exception("response has an unexpected number of fields")
    if "error" not in response:
        raise Exception("response is missing required error field")
    if "result" not in response:
        raise Exception("response is missing required result field")
    if response["error"] is not None:
        raise Exception(response["error"])
    return response["result"]


def create_deck(deck_name):
    invoke("createDeck", deck=deck_name)


def add_note_to_deck(deck_name, front, back):
    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {"Front": front, "Back": back},
        "options": {
            "allowDuplicate": True,
            "duplicateScope": "deck",
            "duplicateScopeOptions": {
                "deckName": deck_name,
                "checkChildren": False,
                "checkAllModels": False,
            },
        },
        "tags": [],
    }
    invoke("addNote", note=note)


def process_csv_files(root_dir, root_deck_name):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".csv"):
                csv_path = os.path.join(dirpath, filename)
                relative_path = os.path.relpath(dirpath, root_dir)
                deck_name = root_deck_name
                if relative_path != ".":
                    deck_name += "::" + relative_path.replace(os.sep, "::")
                deck_name += "::" + os.path.splitext(filename)[0]

                create_deck(deck_name)

                with open(csv_path, newline="", encoding="utf-8") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) == 2:
                            front, back = row
                            add_note_to_deck(deck_name, front, back)


def main():
    parser = argparse.ArgumentParser(
        description="Import flashcards into Anki using AnkiConnect."
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="The root directory containing CSV files.",
    )
    parser.add_argument(
        "--root-deck-name", type=str, required=True, help="The root deck name in Anki."
    )
    args = parser.parse_args()

    process_csv_files(args.input_dir, args.root_deck_name)


if __name__ == "__main__":
    main()
