from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Optional
from reporte import generar_pdf_service
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hola mundo!"}

nombre_temporal = int(time.time() * 1000)
@app.get('/generar-pdf')

async def generar_pdf(id_proceso: int, inicio: int, fin: int, area: int, fecha: str, sede: str, aula: Optional[str] = None, pdf: Optional[str] = nombre_temporal):
    # if not pdf:
    #     pdf = "output"
    try:
        pdf_path = generar_pdf_service(id_proceso, inicio, fin, area, aula, fecha, sede, pdf)
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))