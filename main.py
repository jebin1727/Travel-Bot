from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_bot_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Welcome to Travel Assistant Bot!"}

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    reply = get_bot_response(request.message)
    return {"reply": reply}
