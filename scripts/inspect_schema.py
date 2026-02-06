from pymilvus import connections, Collection, utility
from app.core.config import Config
import os

def inspect_schema():
    # Connect to Milvus
    print(f"Connecting to Milvus at {Config.MILVUS_URI}...")
    connections.connect(
        alias="default", 
        uri=Config.MILVUS_URI, 
        token=Config.MILVUS_TOKEN
    )
    
    collection_name = Config.COLLECTION_NAME
    
    if not utility.has_collection(collection_name):
        print(f"Collection {collection_name} does not exist.")
        return

    # Get Collection Info
    collection = Collection(collection_name)
    print(f"\n--- Schema for {collection_name} ---")
    for field in collection.schema.fields:
        print(f"Field: {field.name}")
        print(f"  Type: {field.dtype}")
        print(f"  Is Primary: {field.is_primary}")
        print(f"  Description: {field.description}")
        print("-" * 20)
        
if __name__ == "__main__":
    inspect_schema()
