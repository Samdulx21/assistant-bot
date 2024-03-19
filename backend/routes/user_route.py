from fastapi import APIRouter
from controllers.user_controller import *
from models.user_model import Users

router = APIRouter()

user = UserController()

@router.get("/users")
async def get_users():
    response = user.get_user()
    return response

@router.get("/user/role")
async def get_patients_user():
    response = user.get_patients_user()
    return response

@router.get("/user/role/{id_p}")
async def get_idpersonal_patients(id_p: int):
    response = user.get_idpersonal_patients(id_p)
    return response

@router.post("/insert/user")
async def insert_user(newuser: Users):
    response = user.insert_user(newuser)
    return response


