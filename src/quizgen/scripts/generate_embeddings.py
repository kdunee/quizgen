import argparse
import json
import logging

from openai import OpenAI
import numpy as np

openai_client = OpenAI()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", required=True, type=str)
    parser.add_argument("--output-path", required=True, type=str)
    parser.add_argument("--embedding-model", type=str, default="text-embedding-3-small")
    args = parser.parse_args()

    with open(args.input_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    all_embeddings = []
    for question in questions:
        question_text = question["question"]
        embedding = (
            openai_client.embeddings.create(
                input=[question_text], model=args.embedding_model
            )
            .data[0]
            .embedding
        )
        all_embeddings.append(embedding)

    all_embeddings = np.array(all_embeddings)

    with open(args.output_path, "wb") as f:
        np.save(f, all_embeddings)
