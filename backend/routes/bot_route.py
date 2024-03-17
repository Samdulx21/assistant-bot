from fastapi import APIRouter, HTTPException
from assistant_bot.chatbot import *
from pydantic import BaseModel

class Message(BaseModel):
    message: str

jarvi = Jarvi()

router = APIRouter()

@router.get("/")
async def root():
    return { "msg": "Welcome to FastApi" }

@router.post("/jarvi")
async def get_response(message: Message):
    user_input = message.message
    response = jarvi.respond(user_input)
    return { "response": response }

