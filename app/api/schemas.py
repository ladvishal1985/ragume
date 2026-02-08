
from pydantic import BaseModel

from typing import List, Optional, Dict

class AgentInput(BaseModel):
    message: str
    session_id: Optional[str] = None
    recent_messages: Optional[List[Dict[str, str]]] = []
    skip_cache: Optional[bool] = False  # Skip semantic cache (for testing)

class IngestInput(BaseModel):
    file_path: Optional[str] = None
    directories: List[str] = []
