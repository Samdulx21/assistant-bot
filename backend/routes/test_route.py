from fastapi import APIRouter, Request, HTTPException, Body
from fastapi.responses import JSONResponse
import json

router = APIRouter()

historial = []  # Lista para almacenar el historial

@router.post("/guardar_historial")
async def guardar_historial(request: Request, data: dict = Body(...)):
    try:
        historial.append(data)  # Agregar los datos recibidos al historial
        return JSONResponse({"message": "Historial guardado exitosamente"})
    except KeyError:
        raise HTTPException(status_code=400, detail="Formato de datos incorrecto")

@router.get("/historial")
async def obtener_historial():
    # Ordenar los datos en el orden deseado
    historial_ordenado = []
    for item in historial:
        historial_ordenado.append({key: item[key] for key in sorted(item.keys())})

    # Generar la respuesta JSON
    return JSONResponse(historial_ordenado)

