
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.core.config import Config
from langchain_milvus import Milvus

def get_llm():
    """Returns the configured LLM instance."""
    if Config.MODEL_PROVIDER == "openai":
        return ChatOpenAI(
            model=Config.OPENAI_LLM_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=0
        )
    else:
        raise ValueError(f"Unsupported provider: {Config.MODEL_PROVIDER}")

def get_embeddings():
    """Returns the configured Embeddings model instance."""
    if Config.MODEL_PROVIDER == "openai":
        return OpenAIEmbeddings(
            model=Config.OPENAI_EMBEDDING_MODEL,
            api_key=Config.OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported provider: {Config.MODEL_PROVIDER}")

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
