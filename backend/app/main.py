from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# IMPORTANTE: Esto permite que React (puerto 5173) hable con Python (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En desarrollo permitimos todo
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analizar")
async def analizar_audio():
    # Aquí simulamos que analizamos un audio
    return {
        "archivo": "evidencia_001.wav",
        "resultado": "Sintético (IA)",
        "probabilidad": 0.94,
        "metadatos": {
            "encoder": "ElevenLabs",
            "bitrate": "128kbps"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)