"""
RAGAS Test Dataset - Minimal Version (3 questions)

Ultra-small dataset to test if RAGAS works at all
"""

from datasets import Dataset

# Test questions with ground truth answers (only 3)
test_data = {
    "question": [
        "What is your Python experience?",
        "What databases do you know?",
        "Do you have React experience?",
    ],
    "ground_truth": [
        "I have 5+ years of Python experience, primarily working with FastAPI and Django for web development, and extensive data processing work.",
        "I have experience with Milvus vector database for semantic search and embeddings storage in my RAG chatbot project.",
        "I don't have React experience in my portfolio.",
    ]
}

# Convert to HuggingFace Dataset format
test_dataset = Dataset.from_dict(test_data)

if __name__ == "__main__":
    print(f"Minimal Test Dataset: {len(test_data['question'])} questions")
