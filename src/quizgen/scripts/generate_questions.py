import argparse
from typing import List
import json
import logging

from openai import OpenAI

openai_client = OpenAI()


def list_concepts(title: str, chapter: str, model: str) -> List[str]:
    concept_extraction_prompt = create_concept_extraction_prompt(title, chapter)
    logging.info("Requesting concepts for %s, using model %s", title, model)
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": concept_extraction_prompt,
            }
        ],
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        max_tokens=16383,
    )
    content = json.loads(chat_completion.choices[0].message.content)
    return content["concepts"]


def generate_questions(chapter: str, concept: str, model: str) -> List[object]:
    quiz_generation_prompt = create_quiz_generation_prompt(chapter, concept)
    logging.info("Requesting questions for %s, using model %s", concept, model)
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": quiz_generation_prompt,
            }
        ],
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        max_tokens=16383,
    )
    content = json.loads(chat_completion.choices[0].message.content)
    return content["questions"]


def create_concept_extraction_prompt(title: str, chapter: str) -> str:
    with open("prompts/concept_extraction.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    prompt = prompt.replace("{{TITLE}}", title)
    prompt = prompt.replace("{{CHAPTER_TEXT}}", chapter)
    return prompt


def create_quiz_generation_prompt(chapter: str, concept: str) -> str:
    with open("prompts/quiz_generation.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    prompt = prompt.replace("{{CHAPTER_TEXT}}", chapter)
    prompt = prompt.replace("{{CONCEPT}}", concept)
    return prompt


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(
        description="Generate questions for a single chapter"
    )
    parser.add_argument(
        "--chapter-path", type=str, required=True, help="Path to the chapter file"
    )
    parser.add_argument(
        "--title", type=str, required=True, help="Title of the course or chapter"
    )
    parser.add_argument(
        "--output", type=str, required=True, help="Path to the output JSON file"
    )
    parser.add_argument(
        "--concept-model",
        type=str,
        default="gpt-4o-mini-2024-07-18",
        help="Model to use for concept extraction",
    )
    parser.add_argument(
        "--questions-model",
        type=str,
        default="gpt-4o-2024-08-06",
        help="Model to use for question generation",
    )
    args = parser.parse_args()

    with open(args.chapter_path, "r", encoding="utf-8") as f:
        chapter = f.read()

    concepts = list_concepts(args.title, chapter, args.concept_model)

    all_questions = []
    for concept in concepts:
        questions = generate_questions(chapter, concept, args.questions_model)
        all_questions.extend(questions)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=4)
