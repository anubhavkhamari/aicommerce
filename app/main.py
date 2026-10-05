from fastapi import FastAPI
from app.api.chat import router as chatRouter

app = FastAPI(
    title = "AI Commerce App",
    version= "0.1.0"
)

@app.get('/')
async def health():
    return {
        "status" : "ok",
        "message" : "API Running ..."
    }

app.include_router(chatRouter)

@app.get('/health')
async def health():
    return {
        "status" : "ok",
        "message" : "@health-enpoint - API Running ..."
    }
