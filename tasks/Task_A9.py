from sentence_transformers import SentenceTransformer, util

def find_most_similar_comments(input_file: str, output_file: str, similarity_type: str = "most"):
    """
    Find a pair of comments that are either most similar or least similar using sentence embeddings.
    
    Parameters:
      - input_file: File containing comments (one per line).
      - output_file: File to write the selected pair of comments.
      - similarity_type: "most" (default) for most similar comments,
                         "least" for least similar comments.
    """
    # Load a pre-trained model (offline)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Read comments and filter out empty lines
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f.readlines() if line.strip()]

    if len(comments) < 2:
        print("Not enough comments to compare.")
        return

    # Get embeddings for each comment
    embeddings = model.encode(comments, convert_to_tensor=True)

    # Initialize variables for tracking best pair
    if similarity_type.lower() == "least":
        best_score = float("inf")
    else:
        best_score = -1  # For most similar, start low

    best_pair = ("", "")

    # Compare all pairs of comments
    for i in range(len(comments)):
        for j in range(i + 1, len(comments)):
            sim = util.pytorch_cos_sim(embeddings[i], embeddings[j]).item()
            if similarity_type.lower() == "least":
                if sim < best_score:
                    best_score = sim
                    best_pair = (comments[i], comments[j])
            else:  # Default: "most"
                if sim > best_score:
                    best_score = sim
                    best_pair = (comments[i], comments[j])

    # Write the selected pair of comments to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(best_pair))

    print(f"{similarity_type.capitalize()} similar comments saved to {output_file} with similarity score: {best_score}")

# Example usage:
if __name__ == "__main__":
    # Most similar comments (default behavior)
    find_most_similar_comments(r"C:\Users\kathb\TDS_Project\data\comments.txt",
                           r"C:\Users\kathb\TDS_Project\data\comments_similar.txt")
    
    # Least similar comments
    find_most_similar_comments(r"C:\Users\kathb\TDS_Project\data\comments.txt",
                           r"C:\Users\kathb\TDS_Project\data\comments_least_similar.txt",
                           similarity_type="least")
