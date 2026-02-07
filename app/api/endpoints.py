
import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.api.schemas import AgentInput, IngestInput
from app.graph.nodes import get_vector_store
from app.graph.workflow import app_graph
from app.core.limiter import limiter
from app.core.semantic_cache import semantic_cache

router = APIRouter()

@router.post("/agent")
@limiter.limit("10/minute")
async def run_agent(request: Request, input_data: AgentInput):
    """
    Runs the RAG agent to answer a question with streaming and conversation memory.
    Rate Limit: 10 requests per minute.
    """
    import uuid
    from app.core.conversation_memory import conversation_memory
    
    # Generate session ID if not provided
    session_id = input_data.session_id or str(uuid.uuid4())
    
    # 1. Semantic Cache Check
    cached_answer = await semantic_cache.search(input_data.message)
    if cached_answer:
        # Return as a simple stream for consistency
        async def mock_stream():
            yield cached_answer
        return StreamingResponse(mock_stream(), media_type="text/plain")

    # 2. Retrieve conversation context from Milvus
    conversation_context = await conversation_memory.retrieve_relevant_context(
        query=input_data.message,
        session_id=session_id,
        k=3
    )

    # 3. Run Agent with Streaming
    async def event_generator():
        full_answer = ""
        initial_state = {
            "question": input_data.message,
            "context": [],
            "answer": "",
            "session_id": session_id,
            "conversation_context": conversation_context,
            "recent_messages": input_data.recent_messages or []
        }
        
        try:
            # Stream tokens from the graph
            async for event in app_graph.astream_events(initial_state, version="v1"):
                kind = event["event"]
                
                # Check for LLM stream events
                if kind == "on_chat_model_stream":
                    content = event["data"]["chunk"].content
                    if content:
                        full_answer += content
                        yield content
                        
            # 4. Save to Cache (After stream completes)
            if full_answer:
                await semantic_cache.add(input_data.message, full_answer)
                
            # 5. Store conversation summary if we have enough messages
            recent_messages = input_data.recent_messages or []
            if len(recent_messages) >= 4:  # Every 2 exchanges (4 messages)
                await conversation_memory.store_summary(
                    session_id=session_id,
                    messages=recent_messages
                )
                
        except Exception as e:
            print(f"Streaming error: {e}")
            yield f"Error: {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")

@router.post("/ingest")
@limiter.limit("5/minute")
async def ingest_document(request: Request, input_data: IngestInput):
    """
    Ingests a PDF file into Milvus.
    Rate Limit: 5 requests per minute.
    """
    file_path = input_data.file_path
    directories = input_data.directories
    
    pdf_files = []
    
    # 1. Collect files from direct path
    if file_path and os.path.exists(file_path):
        pdf_files.append(file_path)
        
    # 2. Collect files from directories
    for directory in directories:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(".pdf"):
                        pdf_files.append(os.path.join(root, file))
    
    if not pdf_files:
        raise HTTPException(status_code=404, detail="No PDF files found in provided paths")
        
    try:
        all_splits = []
        
        for pdf_path in pdf_files:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            
            text_splitters = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            splits = text_splitters.split_documents(docs)
            
            # Ensure metadata
            for split in splits:
                split.metadata.setdefault("keywords", "portfolio")
                split.metadata.setdefault("source", pdf_path)
                # ... (keep other defaults if strict schema needed, relying on Milvus auto-fill / None otherwise if flexible)
                # Minimal defaults to ensure insertion
                for field in ["producer", "creator", "creationdate", "author", "moddate", "subject", "title", "trapped", "page_label"]:
                    split.metadata.setdefault(field, "")
                split.metadata.setdefault("total_pages", 0)
                split.metadata.setdefault("page", 0)

            all_splits.extend(splits)
        
        vector_store = get_vector_store()
        if not vector_store:
             raise HTTPException(status_code=500, detail="Vector store not configured")
        
        if all_splits:
            vector_store.add_documents(all_splits)
            
        return {
            "message": f"Successfully processed {len(pdf_files)} files.",
            "total_chunks": len(all_splits),
            "files": pdf_files
        }
        
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
