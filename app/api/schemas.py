
from pydantic import BaseModel

class AgentInput(BaseModel):
    message: str

class IngestInput(BaseModel):
    file_path: str
