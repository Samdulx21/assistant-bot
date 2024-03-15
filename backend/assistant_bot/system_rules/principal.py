import requests
from random import choice
from sistemareglas import *
import json
import os

try:
    ## creacion del objeto
    engine = sistemadereglas()
    ### reset Preparar el motor para la ejecución.
    engine.reset()
    
    ## se pregunta el estado academico
    v_tos_persistente = input("¿Tiene tos persistente? \n  si   no ")
    ## declare agrega un hecho
    ##La función choice(secuencia) elige un valor al azar en un conjunto de elementos.
    engine.declare(reglas(tos_persistente=choice([str(v_tos_persistente)])))
    ## se pregunta el estado financiero
    v_dificultad_respirar = input("¿Experimenta dificultad para respirar? \n si   no ")
    ## declare agrega un hecho
    engine.declare(reglas(dificultad_respirar=choice([str(v_dificultad_respirar)])))

    v_fiebre_reciente = input("¿Ha tenido fiebre recientemente? \n  si   no ")

    engine.declare(reglas(fiebre_reciente=choice([str(v_fiebre_reciente)])))

    v_dolor_pecho = input("¿Ha experimentado dolor en el pecho? \n  si   no ")

    engine.declare(reglas(dolor_pecho=choice([str(v_dolor_pecho)])))

    v_congestion_nasal = input("¿Ha tenido congestión nasal o secreción nasal? \n  si   no ")

    engine.declare(reglas(congestion_nasal=choice([str(v_congestion_nasal)])))

    ## correr el programa
    engine.run()
    
    # Verificar si el archivo historial.json existe
    if not os.path.exists('historial.json'):
        # Si no existe, crear un archivo vacío
        with open('historial.json', 'w', encoding='utf8') as file:
            file.write('[]')  # Escribir una lista vacía en el archivo JSON
    
    # Crear un diccionario con los datos del resultado actual
    resultado_dict = {
        "¿Tiene tos persistente?": v_tos_persistente,
        "¿Experimenta dificultad para respirar?": v_dificultad_respirar,
        "¿Ha tenido fiebre recientemente?": v_fiebre_reciente,
        "¿Ha experimentado dolor en el pecho?": v_dolor_pecho,
        "¿Ha tenido congestión nasal o secreción nasal?": v_congestion_nasal,
        "respuestas": engine.respuestas
    }
    
    # Enviar los resultados al endpoint en Flask
    url = 'http://localhost:8000/guardar_historial'  # Reemplaza esto con la URL de tu endpoint
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(resultado_dict), headers=headers)
    
    # Abrir el archivo JSON en modo de escritura y lectura ('r+') para agregar los resultados al final del archivo
    with open('historial.json', 'r+', encoding='utf8') as file:
        # Cargar el contenido existente del archivo como una lista de diccionarios
        historial = json.load(file)
        
        # Agregar el resultado actual a la lista de historiales
        historial.append(resultado_dict)
        
        # Posicionar el cursor al inicio del archivo
        file.seek(0)
        
        # Escribir la lista actualizada de historiales en el archivo
        json.dump(historial, file, indent=4, ensure_ascii=False)
        
        # Truncar cualquier contenido adicional que pueda estar presente después de la escritura
        file.truncate()
        
    print(response.json())
    print("Historial guardado en historial.json")
    
except Exception as e:
    print(f"Error: {e}")
