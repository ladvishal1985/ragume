"""
Simple RAG Evaluation - No RAGAS Required

This script collects RAG results and saves them for manual review.
You can compare answers to ground truth yourself without complex metrics.
"""

import asyncio
import json
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.graph.workflow import app_graph
from tests.ragas_test_data import test_dataset

async def evaluate_rag():
    """Collect RAG results and save for review"""
    
    print("="*60)
    print("SIMPLE RAG EVALUATION")
    print("="*60)
    print(f"Test cases: {len(test_dataset)}\n")
    
    results = []
    
    for i, item in enumerate(test_dataset):
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        print(f"[{i+1}/{len(test_dataset)}] {question[:60]}...")
        
        initial_state = {
            "question": question,
            "context": [],
            "answer": "",
            "session_id": "test",
            "conversation_context": [],
            "recent_messages": []
        }
        
        try:
            final_state = await app_graph.ainvoke(initial_state)
            answer = final_state["answer"]
            
            results.append({
                "question": question,
                "ground_truth": ground_truth,
                "rag_answer": answer,
                "match": "OK" if any(word in answer.lower() for word in ground_truth.lower().split()[:5]) else "?"
            })
            
            print(f"  [OK] Got answer")
            
        except Exception as e:
            print(f"  [ERROR] Error: {e}")
            results.append({
                "question": question,
                "ground_truth": ground_truth,
                "rag_answer": f"ERROR: {e}",
                "match": "ERR"
            })
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(test_dataset),
        "results": results
    }
    
    output_dir = os.path.join("tests", "reports")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "rag_evaluation_results.json")
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['question'][:50]}...")
        print(f"   Match: {result['match']}")
    
    print(f"\n[OK] Detailed results saved to: {output_file}")
    print("\nYou can now:")
    print("1. Review the JSON file to compare answers")
    print("2. Run this again after improvements to see changes")
    print("3. Use the comparison script to track progress")

if __name__ == "__main__":
    asyncio.run(evaluate_rag())
