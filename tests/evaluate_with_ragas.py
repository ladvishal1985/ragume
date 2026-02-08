"""
RAGAS Evaluation Script for Portfolio RAG Chatbot

This script evaluates the RAG system's accuracy using RAGAS metrics:
- Faithfulness: No hallucination
- Answer Relevancy: Addresses the question
- Context Precision: Retrieved docs are relevant
- Context Recall: All needed info retrieved
- Answer Similarity: Semantic match to ground truth
- Answer Correctness: Factual accuracy

Usage:
    python tests/evaluate_with_ragas.py
"""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.graph.workflow import app_graph
from tests.ragas_test_data import test_dataset
from app.core.config import Config
import time

# Configure RAGAS with LLM and embeddings
ragas_llm = ChatOpenAI(
    model=Config.OPENAI_LLM_MODEL, 
    api_key=Config.OPENAI_API_KEY,
    temperature=0,
    max_retries=3,  # Retry on failures
    timeout=60  # Increase timeout
)
ragas_embeddings = OpenAIEmbeddings(
    model=Config.OPENAI_EMBEDDING_MODEL, 
    api_key=Config.OPENAI_API_KEY,
    max_retries=3  # Retry on failures
)


async def collect_rag_results(test_dataset):
    """Run RAG system on test questions and collect results."""
    
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    print("="*60)
    print("COLLECTING RAG RESULTS")
    print("="*60)
    
    for i, item in enumerate(test_dataset):
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        print(f"\n[{i+1}/{len(test_dataset)}] Processing: {question[:60]}...")
        
        # Run RAG system directly (bypasses API, so no cache involved)
        # Must provide all required State fields
        initial_state = {
            "question": question,
            "context": [],
            "answer": "",
            "session_id": "ragas_test",  # Required by State
            "conversation_context": [],  # Required by State
            "recent_messages": []  # Required by State
        }
        
        try:
            print(f"  → Calling RAG graph...")
            final_state = await app_graph.ainvoke(initial_state)
            print(f"  → RAG graph completed")
            
            # Collect results
            questions.append(question)
            answers.append(final_state["answer"])
            
            # Extract context (retrieved documents)
            context_docs = final_state.get("context", [])
            context_text = [doc.page_content for doc in context_docs]
            contexts.append(context_text)
            
            ground_truths.append(ground_truth)
            
            print(f"  ✓ Answer: {final_state['answer'][:100]}...")
            print(f"  ✓ Context docs: {len(context_text)}")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            import traceback
            traceback.print_exc()
            # Add empty results to maintain alignment
            questions.append(question)
            answers.append("")
            contexts.append([])
            ground_truths.append(ground_truth)
    
    # Create results dataset
    results = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    return Dataset.from_dict(results)


async def run_ragas_evaluation():
    """Run RAGAS evaluation on RAG system."""
    
    print("\n" + "="*60)
    print("RAGAS EVALUATION - Portfolio RAG Chatbot")
    print("="*60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test cases: {len(test_dataset)}")
    
    # Note: Cache is automatically bypassed when calling graph directly
    print("\n✓ Calling RAG graph directly (bypasses API cache layer)")
    print("  Testing actual RAG system without cached responses\n")
    
    # Collect RAG results
    print("\n" + "-"*60)
    results_dataset = await collect_rag_results(test_dataset)
    
    # Define metrics to evaluate (reduced to 2 to avoid rate limits)
    # Using only the most important metrics
    metrics = [
        faithfulness,           # No hallucination (most critical)
        answer_relevancy,       # Addresses question (second most critical)
        # Commented out to reduce API calls:
        # context_precision,    # Retrieved docs are relevant
        # context_recall,       # All needed info retrieved
    ]
    
    print(f"\nNote: Using 2 metrics (faithfulness, answer_relevancy) to avoid rate limits")
    print(f"Expected API calls: ~{len(test_dataset) * 2 * 5} calls")
    
    # Run evaluation
    print("\n" + "-"*60)
    print("RUNNING RAGAS EVALUATION...")
    print("-"*60)
    
    try:
        # Note: Running evaluation sequentially to avoid rate limits
        print("Note: Evaluation may take a few minutes (avoiding rate limits)...\n")
        
        evaluation_result = evaluate(
            results_dataset,
            metrics=metrics,
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            raise_exceptions=False  # Continue on errors
        )
        
        # Print results
        print("\n" + "="*60)
        print("RAGAS EVALUATION RESULTS")
        print("="*60)
        
        results_dict = {}
        for metric_name, score in evaluation_result.items():
            print(f"{metric_name:.<40} {score:.4f}")
            results_dict[metric_name] = float(score)
        
        # Calculate overall score
        overall_score = sum(results_dict.values()) / len(results_dict)
        print(f"{'Overall Score':.<40} {overall_score:.4f}")
        results_dict["overall"] = overall_score
        
        # Interpret results
        print("\n" + "-"*60)
        print("INTERPRETATION")
        print("-"*60)
        
        def interpret_score(score):
            if score >= 0.90:
                return "Excellent ✓"
            elif score >= 0.80:
                return "Good"
            elif score >= 0.70:
                return "Fair"
            else:
                return "Needs Improvement"
        
        for metric_name, score in results_dict.items():
            if metric_name != "overall":
                interpretation = interpret_score(score)
                print(f"{metric_name}: {interpretation}")
        
        # Save results
        output_file = "tests/ragas_results.json"
        results_to_save = {
            "timestamp": datetime.now().isoformat(),
            "test_cases": len(test_dataset),
            "metrics": results_dict,
            "interpretation": {
                metric: interpret_score(score) 
                for metric, score in results_dict.items()
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(results_to_save, f, indent=2)
        
        print(f"\n✓ Results saved to {output_file}")
        
        return evaluation_result
        
    except Exception as e:
        print(f"\n✗ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(run_ragas_evaluation())
