
from typing import TypedDict, List
from langchain_core.documents import Document

class State(TypedDict):
    """
    State for the RAG agent.
    - question: The user's input question.
    - context: Retrieved context from Milvus.
    - answer: Generated answer.
    """
    question: str
    context: List[Document]
    answer: str
