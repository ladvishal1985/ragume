
import os
from fastapi import APIRouter, HTTPException, Request
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.api.schemas import AgentInput, IngestInput
from app.graph.nodes import get_vector_store
from app.core.limiter import limiter
from app.core.semantic_cache import semantic_cache

router = APIRouter()

@router.post("/agent")
@limiter.limit("10/minute")
async def run_agent(request: Request, input_data: AgentInput):
    """
    Runs the RAG agent to answer a question.
    Rate Limit: 10 requests per minute.
    """
    # 1. Semantic Cache Check
    cached_answer = await semantic_cache.search(input_data.message)
    if cached_answer:
        return {"response": cached_answer, "source": "cache"}

    # 2. Run Agent
    initial_state = {"question": input_data.message, "context": [], "answer": ""}
    final_state = await app_graph.ainvoke(initial_state)
    answer = final_state["answer"]
    
    # 3. Save to Cache (Async background task would be better, but direct await is fine for now)
    await semantic_cache.add(input_data.message, answer)
    
    return {"response": answer, "source": "live"}

@router.post("/ingest")
@limiter.limit("5/minute")
async def ingest_document(request: Request, input_data: IngestInput):
    """
    Ingests a PDF file into Milvus.
    Rate Limit: 5 requests per minute.
    """
    file_path = input_data.file_path
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        text_splitters = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitters.split_documents(docs)
        
        # Ensure all schema fields are present to prevent DataNotMatchException
        for split in splits:
            # Strings (Type 21)
            split.metadata.setdefault("producer", "")
            split.metadata.setdefault("creator", "")
            split.metadata.setdefault("creationdate", "")
            split.metadata.setdefault("author", "")
            split.metadata.setdefault("keywords", "portfolio")
            split.metadata.setdefault("moddate", "")
            split.metadata.setdefault("subject", "history")
            split.metadata.setdefault("title", "")
            split.metadata.setdefault("trapped", "")
            split.metadata.setdefault("source", file_path) # PyPDF usually sets this
            split.metadata.setdefault("page_label", "")
            
            # Ints (Type 5)
            split.metadata.setdefault("total_pages", 0)
            split.metadata.setdefault("page", 0) # PyPDF usually sets this
        
        vector_store = get_vector_store()
        if not vector_store:
             raise HTTPException(status_code=500, detail="Vector store not configured")
             
        # Add documents - Milvus wrapper handles async internal checks usually, but add_documents is sync in base class
        # However, for consistency and thread pool avoidance, we wrap it or just leave it if it's sync.
        # But 'run_agent' definitely needs to be async.
        # Let's make this async too for standard practices, although strictly add_documents might be sync blocking.
        # If add_documents is blocking, we might want to run it in a threadpool to avoid blocking the event loop.
        # LangChain's add_documents is often sync. Let's keep it simple for now, as the main issue was the Agent loop check.
        # We'll just mark the endpoint as async to satisfy FastAPI's loop requirements for other things.
        
        vector_store.add_documents(splits)
        return {"message": f"Successfully ingested {len(splits)} chunks from {file_path}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
@limiter.limit("5/minute")
async def get_profile_summary(request: Request):
    """
    Generates a brief professional summary based on ingested documents.
    Rate Limit: 5 requests per minute.
    """
    try:
        # Check if we have any data first
        vector_store = get_vector_store()
        if not vector_store:
             return {"summary": "No profile data available. Please ingest your resume."}
             
        # We can simply ask the agent to summarize
        prompt = "Summarize the professional profile of this candidate in 3-4 concise sentences, highlighting key skills and roles. Write it in the first person (e.g., 'I am a...')."
        
        initial_state = {"question": prompt, "context": [], "answer": ""}
        final_state = await app_graph.ainvoke(initial_state)
        
        # If no documents are found, the agent might hallucinate or say I don't know. 
        # Ideally we'd check if context was retrieved, but for now we rely on the agent's response.
        return {"summary": final_state["answer"]}
        
    except Exception as e:
        # Fail gracefully so the UI doesn't break
        print(f"Error generating summary: {e}")
        return {"summary": "Welcome to my portfolio! Ask me anything about my experience."}
        
@router.get("/schema")
@limiter.limit("5/minute")
async def inspect_schema(request: Request):

    """
    Returns the schema of the Milvus collection to identify missing fields.
    """
    try:
        vector_store = get_vector_store()
        if not vector_store:
            return {"error": "Vector store not connected"}
        
        # Access the underlying collection
        # langchain_milvus.Milvus stores the collection object in .col or we can get it via utility
        # Accessing internal .col might be risky if version changes, but let's try standard way
        
        # Safe way using utility if we had the connection alias, but langchain manages its own.
        # Let's try to get it from the vector_store object.
        
        col = vector_store.col
        if not col:
            return {"error": "Could not access collection object"}
            
        fields = []
        for field in col.schema.fields:
            fields.append({
                "name": field.name,
                "type": str(field.dtype),
                "is_primary": field.is_primary,
                "description": field.description
            })
            
        return {"schema": fields}
        
    except Exception as e:
        return {"error": str(e)}
