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

    if user_input.lower() == 'salir':
        return { "response": "Adiós!" }

    if user_input.lower() == 'ayuda' or user_input.lower() == 'ayudame':
        return { "response": "Claro!, Indicame qué síntomas presentas para poder ayudarte." }

    # Responder usando el chatbot si no hay síntomas específicos mencionados
    if not any(symptom in user_input.lower() for symptom in ['tos', 'respirar', 'fiebre', 'dolor', 'congestión', 'congestion']):
        return { "response": jarvi.respond(user_input) + "\nPor favor comuníquese con su doctor de confianza \n o llame al 605 344444" }

    # Manejar los síntomas usando el sistema de reglas
    symptoms = {
        'tos_persistente': input("¿Tiene tos persistente? (si/no): "),
        'dificultad_respirar': input("¿Experimenta dificultad para respirar? (si/no): "),
        'fiebre_reciente': input("¿Ha tenido fiebre recientemente? (si/no): "),
        'dolor_pecho': input("¿Ha experimentado dolor en el pecho? (si/no): "),
        'congestion_nasal': input("¿Ha tenido congestión nasal o secreción nasal? (si/no): ")
    }

    print("Analizando síntomas...")
    respuestas = jarvi.handle_symptoms(symptoms)
    for respuesta in respuestas:
        print("Jarvi:", respuesta + "\nPor favor comuníquese con su doctor de confianza \n o llame al 605 344444")

    return { "response": respuesta + " Por favor comuníquese con su doctor de confianza o llame al 605 344444" } 

