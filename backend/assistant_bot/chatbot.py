from random import choice
from .sistemareglas import sistemadereglas
from .reglas import reglas
from nltk.chat.util import Chat, reflections
import nltk
import os

nltk.download('punkt')
nltk.download('wordnet')

class Jarvi:
    def __init__(self):
        self.engine = sistemadereglas()
        self.engine.reset()
        self.chatbot = Chat(self.pairs, reflections)

    def respond(self, message):
        response = self.chatbot.respond(message)
        return response

    def handle_symptoms(self, symptoms):
        self.engine.reset()  # Reiniciar el motor de reglas para cada solicitud
        for symptom, value in symptoms.items():
            self.engine.declare(reglas(**{symptom: value}))
        self.engine.run()  # Ejecutar el motor de reglas
        return self.engine.respuestas
    
    pairs =  [
        (
            r'Hola|Buenos dias|Buenas tardes|Buenas noches[\.\-,{´+}{´´}]*',
            [
                'hola, como estas? Soy Jarvi para servirte.', 
                'hola, soy Jarvi para servirte.'
            ]
        ),
        (
            r'Hola me puedes ayudar|me puedes ayudar(?:\?)?',
            [
                'En que puedo ayudarte?.', 
                'si calor, en que puedo servirte?.'
            ]
        ),
        (
            r'Me siento mal|me siento debil|me he sentido muy mal en estos dias[\.\-,{´+}{´´}]*',
            [
                'Dime qué síntomas presentas, Jarvi podría ayudarte.', 
                'Jarvi está aquí para servirte, dime qué síntomas presentas?'
            ]
        ),
        (
            r'gracias|muchas gracias|te lo agradezco[\.\-,{´+}{´´}]*',
            [
                'de nada, deseas algo mas?\n En caso que no, por favor escribe "salir".', 
                'Jarvi siempre está aquí para servirte, deseas algo mas?\n En caso que no, por favor escribe "salir"'
            ]
        ),
        (
            r'(.*)',
            [
                'Lo siento, no entiendo tu pregunta.', 
                'Por favor, reformula tu pregunta.'
            ]
        )
    ]


    def JarviBot():
        jarvi = Jarvi()

        while True:
            user_input = input("Usuario: ")
            if user_input.lower() == 'salir':
                print("Adiós!")
                break

            if user_input.lower() == 'ayuda' or user_input.lower() == 'ayudame':  # Corregí el operador lógico aquí
                print("Claro!, Indicame qué síntomas presentas para poder ayudarte.")
                continue

            # Responder usando el chatbot si no hay síntomas específicos mencionados
            if not any(symptom in user_input.lower() for symptom in ['tos', 'respirar', 'fiebre', 'dolor', 'congestión', 'congestion']):
                print("Jarvi:", jarvi.respond(user_input))
                continue

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

    if __name__ == "__main__":
        JarviBot()
