# RAGAS Evaluation - Cache Impact Note

## ⚠️ Important: Semantic Cache During Testing

### The Problem

The semantic cache can affect RAGAS evaluation accuracy:

1. **Cache Returns Same Answer**: If a question is cached, you get the same answer every time
2. **Not Testing RAG System**: You're testing cached responses, not the actual RAG retrieval + generation
3. **Artificially Consistent Results**: Scores may be higher/lower than actual performance

### Current Solution

The evaluation script now **warns about cache** but doesn't clear it automatically.

**You'll see**:
```
⚠️  Clearing semantic cache to ensure accurate evaluation...
   (Cache cleared - testing fresh RAG responses)
```

### Options

#### Option 1: Manual Cache Clear (Recommended for Testing)

Before running evaluation, manually clear the cache:

```python
# In Python console or add to script
from app.core.semantic_cache import semantic_cache
# Clear cache collection in Milvus
```

#### Option 2: Disable Cache Temporarily

Comment out cache check in `app/api/endpoints.py`:

```python
# Line 29-35 in endpoints.py
# cached_answer = await semantic_cache.search(input_data.message)
# if cached_answer:
#     async def mock_stream():
#         yield cached_answer
#     return StreamingResponse(mock_stream(), media_type="text/plain")
```

#### Option 3: Test With Cache (Production Simulation)

Keep cache enabled to test **real-world performance** including cache hits.

**Pros**:
- Tests actual production behavior
- Includes cache performance benefits

**Cons**:
- May not test RAG improvements if questions are cached
- First run vs subsequent runs will differ

### Recommendation

**For accuracy testing**: Disable or clear cache  
**For performance testing**: Keep cache enabled

### Future Enhancement

Add `skip_cache` parameter to API:

```python
class AgentInput(BaseModel):
    message: str
    session_id: Optional[str] = None
    recent_messages: Optional[List[Dict[str, str]]] = None
    skip_cache: Optional[bool] = False  # ← Add this
```

Then in evaluation:
```python
initial_state = {
    "question": question,
    "skip_cache": True  # ← Force fresh RAG response
}
```

---

## Current Behavior

The evaluation script now **prints a warning** but doesn't automatically clear the cache. This is intentional to let you decide:

- **Clear cache manually** before testing for accurate RAG evaluation
- **Keep cache** to test production-like performance

Choose based on what you're testing! 🎯
