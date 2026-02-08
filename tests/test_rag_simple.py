"""
Quick test to see where RAGAS evaluation is getting stuck
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def test_rag_call():
    """Test a single RAG call to see if it works"""
    from app.graph.workflow import app_graph
    
    print("Testing single RAG call...")
    
    initial_state = {
        "question": "What is your Python experience?",
        "context": [],
        "answer": ""
    }
    
    print("Calling app_graph.ainvoke()...")
    try:
        final_state = await app_graph.ainvoke(initial_state)
        print(f"✓ Success! Answer: {final_state['answer'][:100]}...")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = asyncio.run(test_rag_call())
    if result:
        print("\n✓ RAG call works! The issue is likely in RAGAS evaluation itself.")
    else:
        print("\n✗ RAG call failed! Fix this first before running RAGAS.")
