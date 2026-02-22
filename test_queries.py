import asyncio
import sys
from app.graph.workflow import app_graph

async def test_agent():
    queries = [
        "Hi",
        "Can you tell me about your projects and deployment experience?"
    ]
    
    for q in queries:
        print(f"\n--- Question: {q} ---")
        initial_state = {
            "question": q,
            "context": [],
            "answer": "",
            "session_id": "test_session",
            "conversation_context": [],
            "recent_messages": []
        }
        
        # Test full execution
        try:
            final_state = await app_graph.ainvoke(initial_state)
            print(f"Answer: {final_state['answer']}")
            
            # Print messages for inspection to see tool usage
            for msg in final_state["messages"]:
                print(f"[{msg.type}]: {msg.content}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_agent())
