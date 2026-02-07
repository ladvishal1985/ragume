
from typing import TypedDict, List, Dict
from langchain_core.documents import Document

class State(TypedDict):
    """
    State for the RAG agent.
    - question: The user's input question.
    - context: Retrieved context from Milvus (portfolio data).
    - answer: Generated answer.
    - session_id: Unique session identifier for conversation tracking.
    - conversation_context: Retrieved conversation summaries from Milvus.
    - recent_messages: Last few messages for immediate context and summarization.
    """
    question: str
    context: List[Document]
    answer: str
    session_id: str
    conversation_context: List[Document]
    recent_messages: List[Dict[str, str]]
