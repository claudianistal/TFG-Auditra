from fastapi import APIRouter, UploadFile
from app.core.engine import ForensicEngine

router = APIRouter()
engine = ForensicEngine() # Instanciamos el motor

@router.post("/analyze")
async def analyze_audio(file: UploadFile):
    # 1. Guardar archivo temporalmente
    # 2. engine.analyze_file(ruta_temporal)
    # 3. Retornar JSON al Frontend (React)
    return engine.analyze_file("ruta/al/archivo")