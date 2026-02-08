"""
RAGAS Evaluation - Minimal Test (3 questions, 2 metrics)

This is the absolute minimal version to test if RAGAS works at all.
- Only 3 questions
- Only 2 metrics (faithfulness, answer_relevancy)
- Should take ~30 API calls total
"""

import asyncio
import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.graph.workflow import app_graph
from tests.ragas_test_data_minimal import test_dataset
from app.core.config import Config
import time

# Configure RAGAS
ragas_llm = ChatOpenAI(
    model=Config.OPENAI_LLM_MODEL,
    api_key=Config.OPENAI_API_KEY,
    temperature=0,
    max_retries=3,
    timeout=60
)
ragas_embeddings = OpenAIEmbeddings(
    model=Config.OPENAI_EMBEDDING_MODEL,
    api_key=Config.OPENAI_API_KEY,
    max_retries=3
)

async def collect_rag_results(test_dataset):
    """Run RAG system on test questions"""
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    print("="*60)
    print("COLLECTING RAG RESULTS (MINIMAL TEST)")
    print("="*60)
    
    for i, item in enumerate(test_dataset):
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        print(f"\n[{i+1}/{len(test_dataset)}] {question[:50]}...")
        
        initial_state = {
            "question": question,
            "context": [],
            "answer": "",
            "session_id": "ragas_test",
            "conversation_context": [],
            "recent_messages": []
        }
        
        try:
            final_state = await app_graph.ainvoke(initial_state)
            
            questions.append(question)
            answers.append(final_state["answer"])
            
            context_docs = final_state.get("context", [])
            context_text = [doc.page_content for doc in context_docs]
            contexts.append(context_text)
            
            ground_truths.append(ground_truth)
            
            print(f"  ✓ Got answer ({len(final_state['answer'])} chars)")
            
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            questions.append(question)
            answers.append("")
            contexts.append([])
            ground_truths.append(ground_truth)
    
    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

async def main():
    print("\n" + "="*60)
    print("RAGAS MINIMAL TEST")
    print("="*60)
    print(f"Questions: {len(test_dataset)}")
    print(f"Metrics: 2 (faithfulness, answer_relevancy)")
    print(f"Expected API calls: ~30")
    
    # Collect results
    results = await collect_rag_results(test_dataset)
    
    # Run RAGAS
    print("\n" + "="*60)
    print("RUNNING RAGAS EVALUATION...")
    print("="*60)
    print("This should take ~1-2 minutes...\n")
    
    try:
        evaluation_result = evaluate(
            results,
            metrics=[faithfulness, answer_relevancy],
            llm=ragas_llm,
            embeddings=ragas_embeddings,
            raise_exceptions=False
        )
        
        print("\n" + "="*60)
        print("✓ RAGAS EVALUATION COMPLETED!")
        print("="*60)
        
        for metric, score in evaluation_result.items():
            print(f"{metric:.<40} {score:.4f}")
        
        # Save results
        results_dict = {metric: float(score) for metric, score in evaluation_result.items()}
        output = {
            "timestamp": datetime.now().isoformat(),
            "test_cases": len(test_dataset),
            "metrics": results_dict
        }
        
        with open("tests/ragas_results_minimal.json", 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Results saved to tests/ragas_results_minimal.json")
        
    except Exception as e:
        print(f"\n✗ RAGAS evaluation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
