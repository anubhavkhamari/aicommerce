from app.domain.chat import ChatRequest, ChatResponse
from app.llm.client import LlmClient

class ChatService : 

    def __init__(self, llm_client: LlmClient):
        self.llm_client = llm_client

    async def chat(
            self,
            req_id : str,
            req : ChatRequest
    ) -> ChatResponse : 
        
        messages = [{
            "role" : "system",
            "content" : (
                "You are an AI ecommerce assistant. "
                "Never invent product prices or inventory.")
        },
            {
                "role" : "user",
                "content" : req.message
            }
        ]

        response = await self.llm_client.generate(messages)

        return ChatResponse(
            req_id= req_id,
            conversationId=req.conversationId,
            message=response
        ) 