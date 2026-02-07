"""
Test script to debug semantic cache functionality.
"""
import asyncio
import sys
sys.path.append('.')

from app.core.semantic_cache import semantic_cache
from app.core.config import Config

async def test_cache():
    print("=" * 60)
    print("SEMANTIC CACHE DEBUG TEST")
    print("=" * 60)
    
    # Check configuration
    print(f"\n1. Configuration Check:")
    print(f"   MILVUS_URI: {Config.MILVUS_URI[:50]}..." if Config.MILVUS_URI else "   MILVUS_URI: NOT SET")
    print(f"   MILVUS_TOKEN: {'SET' if Config.MILVUS_TOKEN else 'NOT SET'}")
    print(f"   Collection: {semantic_cache.collection_name}")
    print(f"   Threshold: {semantic_cache.threshold}")
    
    # Test 1: Add to cache
    print(f"\n2. Adding test entry to cache...")
    test_question = "What is your Python experience?"
    test_answer = "I have 5+ years of Python experience working with FastAPI, Django, and data processing."
    
    try:
        await semantic_cache.add(test_question, test_answer)
        print("   [OK] Successfully added to cache")
    except Exception as e:
        print(f"   [FAIL] Failed to add: {e}")
        return
    
    # Test 2: Search for exact match
    print(f"\n3. Searching for exact match...")
    try:
        result = await semantic_cache.search(test_question)
        if result:
            print(f"   [OK] Cache HIT!")
            print(f"   Answer: {result[:100]}...")
        else:
            print(f"   [FAIL] Cache MISS (should have been a hit)")
    except Exception as e:
        print(f"   [FAIL] Search failed: {e}")
    
    # Test 3: Search for similar question
    print(f"\n4. Searching for similar question...")
    similar_question = "Tell me about your experience with Python"
    try:
        result = await semantic_cache.search(similar_question)
        if result:
            print(f"   [OK] Cache HIT (semantic match)!")
            print(f"   Answer: {result[:100]}...")
        else:
            print(f"   [INFO] Cache MISS (semantic similarity might be below threshold)")
    except Exception as e:
        print(f"   [FAIL] Search failed: {e}")
    
    # Test 4: Search for unrelated question
    print(f"\n5. Searching for unrelated question...")
    unrelated_question = "What is the weather today?"
    try:
        result = await semantic_cache.search(unrelated_question)
        if result:
            print(f"   [FAIL] Cache HIT (should have been a miss!)")
        else:
            print(f"   [OK] Cache MISS (correct)")
    except Exception as e:
        print(f"   [FAIL] Search failed: {e}")
    
    # Test 5: Check collection stats
    print(f"\n6. Collection Statistics:")
    try:
        semantic_cache.collection.flush()
        stats = semantic_cache.collection.num_entities
        print(f"   Total entries: {stats}")
    except Exception as e:
        print(f"   Could not get stats: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_cache())
