from pydantic import BaseModel, Field

class ChatRequest(BaseModel) :
    conversationId: str = Field(min_length = 1)
    message: str = Field(min_length=1, max_length=10000)

class ChatResponse(BaseModel):
    req_id: str 
    conversationId: str
    message: str