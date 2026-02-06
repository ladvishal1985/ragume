
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.core.config import Config

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
