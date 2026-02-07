import time
from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from app.core.config import Config
from app.core.factory import get_embeddings

class SemanticCache:
    def __init__(self, collection_name="semantic_cache", threshold=0.75):
        self.collection_name = collection_name
        self.threshold = threshold
        self.dims = 1536 # OpenAI text-embedding-3-small dimension
        self._ensure_connection()
        self.collection = self._get_or_create_collection()

    def _ensure_connection(self):
        if not connections.has_connection("default"):
            connections.connect(
                alias="default", 
                uri=Config.MILVUS_URI, 
                token=Config.MILVUS_TOKEN
            )

    def _get_or_create_collection(self):
        if utility.has_collection(self.collection_name):
            collection = Collection(self.collection_name)
            collection.load()
            return collection

        # Define Schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dims),
            FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=1000),
            FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=65535),
        ]
        schema = CollectionSchema(fields, "Semantic cache for RAG responses")
        
        collection = Collection(self.collection_name, schema)
        
        # Create Index
        index_params = {
            "metric_type": "COSINE",
            "index_type": "AUTOINDEX",
            "params": {}
        }
        collection.create_index(field_name="vector", index_params=index_params)
        collection.load()
        return collection

    async def search(self, question: str):
        """Returns cached answer if similarity > threshold."""
        try:
            embeddings_model = get_embeddings()
            vector = await embeddings_model.aembed_query(question)
            
            search_params = {
                "metric_type": "COSINE", 
                "params": {"radius": self.threshold} # Range search if supported or manual filter
            }
            
            # Basic search
            results = self.collection.search(
                data=[vector], 
                anns_field="vector", 
                param={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=1,
                output_fields=["answer", "question"]
            )
            
            if results and results[0]:
                match = results[0][0]
                # Distance in Milvus with COSINE is 1 - cosine_similarity for some indices, 
                # or straightforward cosine depending on metric.
                # Usually matches return a 'score'. For COSINE, higher is better (closer to 1).
                # Let's verify score.
                
                # Debug logging
                print(f"[Cache] Query: '{question[:50]}...'")
                print(f"[Cache] Best match: '{match.entity.get('question')[:50]}...'")
                print(f"[Cache] Similarity score: {match.score:.4f} (threshold: {self.threshold})")
                
                if match.score >= self.threshold:
                    print(f"[Cache] HIT - Returning cached answer")
                    return match.entity.get("answer")
                else:
                    print(f"[Cache] MISS - Score below threshold")
            
            return None
        except Exception as e:
            print(f"Cache search failed: {e}")
            return None

    async def add(self, question: str, answer: str):
        """Adds a question-answer pair to the cache."""
        try:
            embeddings_model = get_embeddings()
            vector = await embeddings_model.aembed_query(question)
            
            data = [
                [vector], # vector
                [question], # question
                [answer]    # answer
            ]
            
            # Insert usually suggests needing column-based format for pymilvus
            # [ [vector], [question_str], [answer_str] ] ?
            # Pymilvus insert expects list of columns.
            
            insert_data = [
                [vector],   # vector column
                [question], # question column
                [answer]    # answer column
            ]
            
            self.collection.insert(insert_data)
            # For serverless/cloud, flush might be handled or not needed instantly, 
            # but good to ensure data visibility eventually.
        except Exception as e:
            print(f"Cache write failed: {e}")

# Global instance
semantic_cache = SemanticCache()
