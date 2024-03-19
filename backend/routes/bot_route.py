from fastapi import APIRouter, HTTPException, Body
from assistant_bot.chatbot import *
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class SymptomInput(BaseModel):
    tos_persistente: str
    dificultad_respirar: str
    fiebre_reciente: str
    dolor_pecho: str
    congestion_nasal: str

jarvi = Jarvi()

router = APIRouter()


@router.get("/")
async def root():
    return { "msg": "Welcome to FastApi" }

@router.post("/jarvi")
async def get_response(message: Message):
    user_input = message.message
 
    if user_input.lower() == 'salir':
        return { "response": "Adiós!" }
 
    if user_input.lower() == 'ayuda' or user_input.lower() == 'ayudame':
        return { "response": "Claro!, Indicame qué síntomas presentas para poder ayudarte." }
 
    # Responder usando el chatbot si no hay síntomas específicos mencionados
    if not any(symptom in user_input.lower() for symptom in ['tos', 'respirar', 'fiebre', 'dolor', 'congestión', 'congestion']):
        return { "response": jarvi.respond(user_input) }
 
    # Manejar los síntomas usando el sistema de reglas
    symptoms = [
        "¿Tiene tos persistente? (si/no)",
        "¿Experimenta dificultad para respirar? (si/no)",
        "¿Ha tenido fiebre recientemente? (si/no)",
        "¿Ha experimentado dolor en el pecho? (si/no)",
        "¿Ha tenido congestión nasal o secreción nasal? (si/no)"
    ]
    return { "question": symptoms[0] }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="127.0.0.1", port=8000)
