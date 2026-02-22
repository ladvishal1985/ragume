from typing import TypedDict, List, Dict, Annotated, Sequence
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    """
    State for the RAG agent.
    - messages: Conversation messages for the agent (includes tool calls/responses)
    - question: The user's input question.
    - context: Retrieved context from Milvus (portfolio data).
    - answer: Generated answer.
    - session_id: Unique session identifier for conversation tracking.
    - conversation_context: Retrieved conversation summaries from Milvus.
    - recent_messages: Last few messages for immediate context and summarization.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    question: str
    context: List[Document]
    answer: str
    session_id: str
    conversation_context: List[Document]
    recent_messages: List[Dict[str, str]]
