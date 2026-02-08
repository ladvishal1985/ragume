"""
Test Milvus connection to see if that's causing the hang
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("Testing Milvus connection...")

try:
    from app.core.config import Config
    from pymilvus import connections, utility
    
    print(f"Connecting to Milvus at: {Config.MILVUS_URI}")
    
    connections.connect(
        alias="default",
        uri=Config.MILVUS_URI,
        token=Config.MILVUS_TOKEN,
        timeout=5  # 5 second timeout
    )
    
    print("✓ Connected to Milvus!")
    
    # List collections
    collections = utility.list_collections()
    print(f"✓ Collections: {collections}")
    
    connections.disconnect("default")
    print("✓ Milvus is working!")
    
except Exception as e:
    print(f"✗ Milvus connection failed: {e}")
    print("\nThis is likely why RAGAS evaluation is stuck!")
    print("Make sure Milvus is running or check your .env configuration.")
    import traceback
    traceback.print_exc()
