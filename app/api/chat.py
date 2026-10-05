from uuid import uuid4
from fastapi import APIRouter
from app.domain.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.llm.provider import GeminiLlmClient

router = APIRouter()

gemini_llm = GeminiLlmClient()
chat_service = ChatService(llm_client=gemini_llm)

@router.post('/v1/chat', response_model= ChatResponse) 
async def chat(req : ChatRequest) :
    req_id = str(uuid4())

    return await chat_service.chat(
        req= req, 
        req_id = req_id 
    )