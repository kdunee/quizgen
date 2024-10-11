from typing import Tuple, List
import argparse
import os
import csv
from collections import defaultdict

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def thin_out_questions(embeddings, T):
    """
    Thins out a set of question embeddings to approximately T questions, ensuring that the
    selected questions are diverse and not too similar to each other.

    Parameters
    ----------
    embeddings : numpy array
        NxM matrix of N question embeddings, each of size M
    T : int
        The desired number of questions to select

    Returns
    -------
    List of int
        The indices of the selected questions in the original embeddings matrix
    """
    N, M = embeddings.shape

    # If desired number of questions T is greater than or equal to N, return the original set
    if T >= N:
        return list(range(N))

    # Step 1: Compute pairwise cosine similarity between all question embeddings
    similarity_matrix = cosine_similarity(embeddings)

    # Step 2: Initialize a similarity threshold (starting low and adjusting)
    low_threshold = 0.0  # Very relaxed threshold (far apart)
    high_threshold = 0.99  # Tight threshold (almost identical)
    threshold = low_threshold

    # Step 3: Create a function to filter embeddings based on the current threshold
    def filter_questions(similarity_matrix, threshold):
        # We will keep track of the selected questions
        selected = []
        for i in range(N):
            is_distinct = True
            for j in selected:
                # If the similarity is greater than threshold, it's too close to an existing question
                if similarity_matrix[i, j] > threshold:
                    is_distinct = False
                    break
            if is_distinct:
                selected.append(i)
        return selected

    # Step 4: Adjust the threshold to reach approximately T questions
    final_selected_indices = list(range(N))  # Start with all questions if necessary
    while low_threshold <= high_threshold:
        threshold = (low_threshold + high_threshold) / 2.0
        selected_indices = filter_questions(similarity_matrix, threshold)

        if len(selected_indices) == T:
            final_selected_indices = selected_indices
            break  # We found the right threshold
        elif len(selected_indices) > T:
            final_selected_indices = selected_indices  # Save the largest set <= T
            high_threshold = threshold - 0.01  # Too many questions, decrease threshold
        else:
            low_threshold = threshold + 0.01  # Too few questions, increase threshold

    # Step 5: Return the indices of the selected questions
    return final_selected_indices[:T]  # Trim to exactly T


def load_embeddings(directory_path: str) -> Tuple[np.ndarray, List[Tuple[str, int]]]:
    """
    Loads all .npy files from a directory tree and returns a single matrix of
    all the embeddings and an index that maps each row to the original file
    and row number.

    Args:
        directory_path (str): The path to the directory containing the .npy
            files

    Returns:
        A tuple of (combined_embeddings, index) where:

        - combined_embeddings is a numpy matrix of shape (N, M) where N is the
            total number of embeddings and M is the embedding dimension
        - index is a list of tuples (relative_path, row_number) where
            relative_path is the path to the file relative to the input
            directory and row_number is the row number of the embedding in
            the file
    """
    embeddings = []
    index = []
    total_rows = 0

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".npy"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)

                # Load the embeddings from the .npy file
                file_embeddings = np.load(file_path)
                if file_embeddings.shape == (0,):
                    continue

                # Add the embeddings to the list
                embeddings.append(file_embeddings)

                # Create index entries for each embedding in this file
                for i in range(file_embeddings.shape[0]):
                    index.append((relative_path, i))

                total_rows += file_embeddings.shape[0]

    # Concatenate all embeddings into a single matrix
    combined_embeddings = np.concatenate(embeddings, axis=0)

    return combined_embeddings, index


def main():
    parser = argparse.ArgumentParser(
        description="Thin out a set of question embeddings to T questions, ensuring that the selected questions are diverse and not too similar to each other."
    )
    parser.add_argument(
        "--csv-dir", required=True, help="Directory containing CSV files"
    )
    parser.add_argument(
        "--embeddings-dir", required=True, help="Directory containing .npy files"
    )
    parser.add_argument("--output-dir", required=True, help="Output directory")
    parser.add_argument(
        "--T", type=int, default=100, help="Number of questions to select"
    )

    args = parser.parse_args()

    # Load the embeddings
    embeddings, index = load_embeddings(args.embeddings_dir)

    # Thin out the embeddings
    selected_indices = thin_out_questions(embeddings, T=args.T)

    # Create a dictionary to map CSV files to the rows we need to select
    csv_file_rows = defaultdict(list)
    for idx in selected_indices:
        npy_file_path, row_number = index[idx]
        csv_file_path = npy_file_path.replace(".npy", ".csv")
        csv_file_rows[csv_file_path].append(row_number)

    # Read only the necessary CSV files and select the required rows
    selected_questions = []
    for csv_file_path, row_numbers in csv_file_rows.items():
        full_csv_path = os.path.join(args.csv_dir, csv_file_path)
        with open(full_csv_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            content = list(reader)
            for row_number in row_numbers:
                selected_questions.append(content[row_number])

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # Write the selected questions to a new CSV file in the output directory
    output_file_path = os.path.join(
        args.output_dir, f"thinned_out_questions_{args.T}.csv"
    )
    with open(output_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(selected_questions)

    print(
        f"Selected {len(selected_questions)} questions and saved them to {output_file_path}"
    )


if __name__ == "__main__":
    main()
