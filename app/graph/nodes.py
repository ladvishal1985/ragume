from langchain_core.messages import SystemMessage, HumanMessage
from app.core.factory import get_llm
from app.graph.state import State
from app.graph.tools import search_portfolio

tools = [search_portfolio]

async def agent(state: State):
    """Generates an answer using the LLM and available tools."""
    print("Agent is thinking...")
    llm = get_llm().bind_tools(tools)
    
    system_prompt = """You are a professional, friendly, and helpful AI assistant representing the portfolio owner.
Your goal is to answer questions about the owner's skills, experience, and projects. Call the `search_portfolio` tool whenever you need specific information from the portfolio.

Rules:
1. Answer in the first person (e.g., "I have experience in...", "My project involves...").
2. **Be extremely brief and concise by default.** Provide a one or two-sentence summary unless the user explicitly asks for a detailed or long answer.
3. If the user asks for "details", "elaborate", or a "deep dive", then provide a comprehensive answer.
4. If you use a tool and the answer is not found, politely say you don't have that information. Do NOT hallucinate.
5. Maintain a professional and engaging tone.
"""
    
    # Format conversation context if any
    conv_history_str = ""
    docs = state.get("conversation_context", [])
    if docs:
        conv_history_str = "Relevant Conversation History:\n"
        for doc in docs:
            conv_history_str += f"- {doc.page_content}\n"
    
    if conv_history_str:
        system_prompt += f"\n\n{conv_history_str}"
        
    sys_msg = SystemMessage(content=system_prompt)
    
    messages = state.get("messages", [])
    if not messages:
        question = (state.get("question") or "").strip()
        if not question:
            raise ValueError("State must include a non-empty 'question' or initial 'messages'.")
        messages = [HumanMessage(content=question)]
    
    # Process with LLM
    response = await llm.ainvoke([sys_msg] + messages)
    
    # Extract text content for compatibility with summary endpoint
    answer_text = response.content if isinstance(response.content, str) else ""
    
    return {"messages": [response], "answer": answer_text}

def get_vector_store():
    # Only keeping this stub for backward compatibility with endpoints if needed directly
    from app.core.factory import get_vector_store as factory_get_vector_store
    return factory_get_vector_store()
