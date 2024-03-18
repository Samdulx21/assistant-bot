from fastapi import APIRouter, HTTPException
from controllers.login_controller import *
from models.user_model import LoginModel

router = APIRouter()

login = LoginController()

@router.post("/login")
async def login_user(userlogin: LoginModel):
    response = login.login_user(userlogin)
    return response







