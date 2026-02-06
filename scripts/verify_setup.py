import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import Config
from app.core.factory import get_embeddings
from langchain_milvus import Milvus

def check_connections():
    print("--- Verifying RAG Setup ---")
    
    # 1. Check Configuration
    print("\n1. Checking Environment Variables...")
    print(f"MODEL_PROVIDER: {Config.MODEL_PROVIDER}")
    print(f"OPENAI_API_KEY: {'Set' if Config.OPENAI_API_KEY else 'Missing'}")
    print(f"MILVUS_URI: {'Set' if Config.MILVUS_URI else 'Missing'}")
    print(f"MILVUS_TOKEN: {'Set' if Config.MILVUS_TOKEN else 'Missing'}")
    
    if not Config.OPENAI_API_KEY:
        print("[ERROR] OPENAI_API_KEY is missing.")
        return
    if not Config.MILVUS_URI:
        print("[ERROR] MILVUS_URI is missing.")
        return

    # 2. Check OpenAI
    print("\n2. Testing OpenAI Connection (Embeddings)...")
    try:
        embeddings = get_embeddings()
        vector = embeddings.embed_query("test connection")
        print(f"[SUCCESS] OpenAI Embeddings working. Vector length: {len(vector)}")
    except Exception as e:
        print(f"[ERROR] OpenAI Error: {e}")
        return

    # 3. Check Milvus
    print("\n3. Testing Milvus Connection...")
    try:
        # Trying to initialize the vector store which connects to Milvus
        vector_store = Milvus(
            embedding_function=embeddings,
            connection_args={
                "uri": Config.MILVUS_URI,
                "token": Config.MILVUS_TOKEN,
            },
            collection_name=Config.COLLECTION_NAME,
            auto_id=True,
        )
        print(f"[SUCCESS] Milvus wrapper initialized for collection: {Config.COLLECTION_NAME}")
        
    except Exception as e:
        print(f"[ERROR] Milvus Error: {e}")
        return

    print("\n[SUCCESS] Verification Complete: Credentials appear valid.")

if __name__ == "__main__":
    check_connections()
