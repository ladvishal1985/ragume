
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Model Provider: 'openai', 'google', etc.
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai").lower()
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")

    # Milvus / Zilliz Cloud Settings
    MILVUS_URI = os.getenv("MILVUS_URI")
    MILVUS_TOKEN = os.getenv("MILVUS_TOKEN")
    COLLECTION_NAME = os.getenv("MILVUS_COLLECTION", "portfolio_rag")

    @classmethod
    def validate(cls):
        """Simple validation to ensure critical keys are present based on provider."""
        if cls.MODEL_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is missing in environment variables.")
        
        if not cls.MILVUS_URI or not cls.MILVUS_TOKEN:
             # Warning only, as user might fill this later
             print("WARNING: MILVUS_URI or MILVUS_TOKEN is missing.")
