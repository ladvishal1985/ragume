
from langchain_milvus import Milvus
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.factory import get_llm, get_embeddings
from app.core.config import Config
from datetime import datetime
from typing import List, Dict
import re

class ConversationMemory:
    """Manages conversation summaries with Milvus vector storage."""
    
    def __init__(self):
        self.embeddings = get_embeddings()
        self.llm = get_llm()
        self.collection_name = "conversation_memory"
        
        # Initialize Milvus vector store
        if not Config.MILVUS_URI or not Config.MILVUS_TOKEN:
            print("Warning: Milvus not configured. Conversation memory disabled.")
            self.vector_store = None
            return
            
        try:
            self.vector_store = Milvus(
                embedding_function=self.embeddings,
                connection_args={
                    "uri": Config.MILVUS_URI,
                    "token": Config.MILVUS_TOKEN,
                },
                collection_name=self.collection_name,
                auto_id=True,
            )
            print(f"Conversation memory initialized with collection: {self.collection_name}")
        except Exception as e:
            print(f"Error initializing conversation memory: {e}")
            self.vector_store = None
    
    async def summarize_conversation(self, messages: List[Dict[str, str]]) -> str:
        """
        Summarize a conversation exchange using LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Concise summary string
        """
        template = """Summarize the following conversation exchange concisely.
Focus on:
- Key topics discussed
- Questions asked by the user
- Important information shared by the assistant

Keep the summary under 100 words and write in third person.

Conversation:
{conversation}

Summary:"""
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Format conversation
        conversation_text = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in messages
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        summary = await chain.ainvoke({"conversation": conversation_text})
        
        return summary.strip()
    
    async def store_summary(self, session_id: str, messages: List[Dict[str, str]]):
        """
        Store conversation summary in Milvus.
        
        Args:
            session_id: Unique session identifier
            messages: List of messages to summarize
        """
        if not self.vector_store:
            print("Conversation memory not available. Skipping summary storage.")
            return
        
        try:
            # Generate summary
            summary = await self.summarize_conversation(messages)
            
            # Extract topics (simple keyword extraction)
            topics = self._extract_topics(summary)
            
            # Create metadata
            metadata = {
                "session_id": session_id,
                "summary": summary,
                "timestamp": str(int(datetime.utcnow().timestamp() * 1000)),  # Unix timestamp in ms
                "message_count": str(len(messages)),
                "topics": ",".join(topics)
            }
            
            # Store in Milvus
            self.vector_store.add_texts(
                texts=[summary],
                metadatas=[metadata]
            )
            
            print(f"Stored conversation summary for session {session_id[:20]}... ({len(messages)} messages)")
            
        except Exception as e:
            print(f"Error storing conversation summary: {e}")
    
    async def retrieve_relevant_context(
        self, 
        query: str, 
        session_id: str, 
        k: int = 3
    ) -> List:
        """
        Retrieve relevant conversation summaries for a given query.
        
        Args:
            query: Current user question
            session_id: Session to filter by
            k: Number of summaries to retrieve
            
        Returns:
            List of Document objects with relevant summaries
        """
        if not self.vector_store:
            return []
        
        try:
            # Create retriever with session filter
            retriever = self.vector_store.as_retriever(
                search_kwargs={
                    "k": k,
                    "expr": f'session_id == "{session_id}"'  # Filter by session
                }
            )
            
            docs = await retriever.ainvoke(query)
            
            if docs:
                print(f"Retrieved {len(docs)} conversation summaries for session {session_id[:20]}...")
            
            return docs
            
        except Exception as e:
            print(f"Error retrieving conversation context: {e}")
            return []
    
    def _extract_topics(self, text: str) -> List[str]:
        """
        Extract key topics from summary text.
        Simple implementation using capitalized words and common tech terms.
        
        Args:
            text: Summary text
            
        Returns:
            List of topic keywords
        """
        # Extract capitalized words (likely proper nouns/topics)
        capitalized = re.findall(r'\b[A-Z][a-z]+\b', text)
        
        # Common tech keywords to look for
        tech_keywords = [
            'Python', 'FastAPI', 'React', 'JavaScript', 'TypeScript',
            'Docker', 'AWS', 'API', 'database', 'frontend', 'backend',
            'authentication', 'deployment', 'testing', 'AI', 'ML'
        ]
        
        found_keywords = [kw for kw in tech_keywords if kw.lower() in text.lower()]
        
        # Combine and deduplicate
        topics = list(set(capitalized + found_keywords))
        
        # Return top 5
        return topics[:5]


# Global instance
conversation_memory = ConversationMemory()
