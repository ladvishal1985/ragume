
from langchain_milvus import Milvus
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import Config
from app.core.factory import get_llm, get_embeddings
from app.graph.state import State

def get_vector_store():
    """Initializes and returns the Milvus vector store connection."""
    embeddings = get_embeddings()
    
    if not Config.MILVUS_URI or not Config.MILVUS_TOKEN:
        print("Milvus URI/Token not set. Vector store usage will fail.")
        return None

    vector_store = Milvus(
        embedding_function=embeddings,
        connection_args={
            "uri": Config.MILVUS_URI,
            "token": Config.MILVUS_TOKEN,
        },
        collection_name=Config.COLLECTION_NAME,
        auto_id=True,
    )
    return vector_store

async def retrieve(state: State):
    """Retrieves relevant documents from Milvus."""
    print(f"Retrieving for: {state['question']}")
    vector_store = get_vector_store()
    if not vector_store:
        return {"context": []}
        
    retriever = vector_store.as_retriever(search_kwargs={"k": 6})
    docs = await retriever.ainvoke(state["question"])
    return {"context": docs}

async def generate(state: State):
    """Generates an answer using the LLM, retrieved context, and conversation history."""
    print("Generating answer...")
    llm = get_llm()
    
    template = """You are a professional, friendly, and helpful AI assistant representing the portfolio owner.
Your goal is to answer questions about the owner's skills, experience, and projects based on the provided context.

{conversation_context_section}

Rules:
1. Answer in the first person (e.g., "I have experience in...", "My project involves...").
2. Be concise but comprehensive. Prioritize specific details like technologies used, dates, and outcomes.
3. If the answer is not in the context, politely say you don't have that information. Do NOT hallucinate.
4. Maintain a professional and engaging tone.
5. Use the conversation history to understand follow-up questions and maintain context.

Portfolio Context:
{context}

Current Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    
    # Helper to format docs
    def format_docs(docs):
        if not docs:
            return "No relevant portfolio information found."
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Helper to format conversation context
    def format_conversation_context(docs):
        if not docs:
            return ""
        formatted = "Relevant Conversation History:\n"
        for doc in docs:
            formatted += f"- {doc.page_content}\n"
        return formatted + "\n"
    
    chain = (
        {
            "context": lambda x: format_docs(state["context"]),
            "question": lambda x: state["question"],
            "conversation_context_section": lambda x: format_conversation_context(
                state.get("conversation_context", [])
            )
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = await chain.ainvoke(state)
    return {"answer": response}
