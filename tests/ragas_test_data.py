"""
RAGAS Test Dataset for Portfolio RAG Chatbot

This file contains test questions with ground truth answers for evaluating
the RAG system's accuracy using RAGAS metrics.
"""

from datasets import Dataset

# Test questions with ground truth answers
test_data = {
    "question": [
        # Simple questions - Basic information retrieval
        "What is your Python experience?",
        "What databases do you know?",
        "Do you have React experience?",
        
        # Complex questions - Multiple pieces of information
        "What Python projects have you built and how did you deploy them?",
        "Tell me about your experience with APIs and FastAPI",
        
        # Technical questions - Specific implementations
        "How did you implement conversation memory in your chatbot?",
        "What vector database did you use and why?",
        "How does your semantic cache work?",
        
        # Edge cases - Testing boundaries
        "What is your experience with machine learning?",
        "Tell me about your mobile app development experience",
    ],
    "ground_truth": [
        # Simple questions - Ground truth answers
        "I have over 5 years of Python experience, specializing in FastAPI and Django for web development.",
        
        "I primarily use Milvus for vector storage and semantic search in my RAG chatbot projects.",
        
        "No, I don't have React experience listed in my portfolio.",
        
        # Complex questions - Ground truth answers
        "I built Ragume, a RAG chatbot using FastAPI and LangChain, which I deployed on Render.",
        
        "I have extensive experience with APIs and FastAPI, including building the production backend for my Ragume chatbot.",
        
        # Technical questions - Ground truth answers
        "I implemented conversation memory using semantic retrieval of lesson summaries stored in Milvus.",
        
        "I use Milvus as my vector database for its efficient semantic search and seamless integration with LangChain.",
        
        "My semantic cache uses Milvus to store and retrieve previously generated answers based on query similarity.",
        
        # Edge cases - Ground truth answers
        "I don't have direct machine learning experience, though I utilize LLMs through APIs for my RAG projects.",
        
        "I do not have mobile app development experience in my portfolio.",
    ]
}

# Convert to HuggingFace Dataset format
test_dataset = Dataset.from_dict(test_data)

# Print dataset info
if __name__ == "__main__":
    print(f"Test Dataset Created:")
    print(f"  Total questions: {len(test_data['question'])}")
    print(f"\nSample question:")
    print(f"  Q: {test_data['question'][0]}")
    print(f"  A: {test_data['ground_truth'][0]}")
