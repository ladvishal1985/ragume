from langchain_core.tools import tool
from app.core.factory import get_vector_store

@tool
async def search_portfolio(query: str) -> str:
    """Searches the portfolio for information about the owner's skills, experience, and projects.
    Use this tool whenever you need to find specific information from the portfolio to answer the user's question.
    """
    vector_store = get_vector_store()
    if not vector_store:
        return "Error: Vector store is not available."
    
    retriever = vector_store.as_retriever(search_kwargs={"k": 6})
    docs = await retriever.ainvoke(query)
    
    if not docs:
        return "No relevant portfolio information found."
        
    return "\n\n".join(doc.page_content for doc in docs)
