
from pydantic import BaseModel

from typing import List, Optional

class AgentInput(BaseModel):
    message: str

class IngestInput(BaseModel):
    file_path: Optional[str] = None
    directories: List[str] = []
