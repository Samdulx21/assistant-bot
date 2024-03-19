from fastapi import APIRouter, HTTPException, Request
from assistant_bot.chatbot import Jarvi
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class SymptomInput(BaseModel):
    tos_persistente: str
    dificultad_respirar: str
    fiebre_reciente: str
    dolor_pecho: str
    congestion_nasal: str

async def ask_yes_no_helper(request: Request, question: str) -> bool:
    """
    Función que pregunta al usuario una pregunta de sí/no y devuelve la respuesta.

    Parámetros:
        request: Objeto de solicitud de FastAPI que contiene la información de la solicitud HTTP.
        question: La pregunta que se le hará al usuario.

    Retorno:
        True si el usuario responde "sí", False si responde "no".

    Excepciones:
        HTTPException 400: Si la solicitud no contiene una respuesta válida.
    """

    try:
        # Obtener la respuesta del usuario de la solicitud
        data = await request.json()
        respuesta = data["respuesta"].lower()
    except KeyError:
        # La solicitud no contiene la respuesta
        raise HTTPException(status_code=400, detail="La solicitud debe contener una respuesta 'sí' o 'no'.")

    if respuesta not in ("sí", "no"):
        # La respuesta no es válida
        raise HTTPException(status_code=400, detail="La respuesta debe ser 'sí' o 'no'.")

    return respuesta == "sí"


jarvi = Jarvi()
router = APIRouter()


@router.get("/")
async def root():
    return { "msg": "Welcome to FastApi" }

@router.post("/jarvi")
async def get_response(request: Request, message: Message):
    user_input = message.message
 
    if user_input.lower() == 'salir':
        return { "response": "Adiós!" }
 
    if user_input.lower() == 'ayuda' or user_input.lower() == 'ayudame':
        return { "response": "Claro!, Indicame qué síntomas presentas para poder ayudarte." }
 
    # Responder usando el chatbot si no hay síntomas específicos mencionados
    if not any(symptom in user_input.lower() for symptom in ['tos', 'respirar', 'fiebre', 'dolor', 'congestión', 'congestion']):

        response = jarvi.respond(user_input)
        return { "response": response }


    def ask_yes_no(question):
        return ask_yes_no_helper(request, question)


    symptoms = {
        'tos_persistente': await ask_yes_no_helper(request, "¿Tiene tos persistente? (si/no): "),
        'dificultad_respirar': await ask_yes_no_helper(request, "¿Experimenta dificultad para respirar? (si/no): "),
        'fiebre_reciente': await ask_yes_no_helper(request, "¿Ha tenido fiebre recientemente? (si/no): "),
        'dolor_pecho': await ask_yes_no_helper(request, "¿Ha experimentado dolor en el pecho? (si/no): "),
        'congestion_nasal': await ask_yes_no_helper(request, "¿Ha tenido congestión nasal o secreción nasal? (si/no): ")
    }

    respuestas = jarvi.handle_symptoms(symptoms)

    return { "response": respuestas }

        return { "response": jarvi.respond(user_input) }
 
    # Manejar los síntomas usando el sistema de reglas
    questions = [
        "¿Tiene tos persistente? (si/no)",
        "¿Experimenta dificultad para respirar? (si/no)",
        "¿Ha tenido fiebre recientemente? (si/no)",
        "¿Ha experimentado dolor en el pecho? (si/no)",
        "¿Ha tenido congestión nasal o secreción nasal? (si/no)"
    ]
    return { "question": questions[0] }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(router, host="127.0.0.1", port=8000)

