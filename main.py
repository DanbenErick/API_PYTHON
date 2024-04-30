from fastapi import FastAPI, HTTPException
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import time
from typing import Optional
from padron import generar_pdf_service, generar_pdf_bloque_service
from resultados import generar_pdf_resultados
from constancia import generar_constancias_por_proceso, generar_constancia_por_estudiante
from reporte_cordinador import generar_reporte_por_cordinador
from reporte_aulas import generar_reporte_por_aula

import json
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
@app.get('/generar-pdf-bloque')
async def generar_pdf_bloque(data, pdf: Optional[str] = nombre_temporal):
    
    # if not pdf:
    #     pdf = "output"
    try:
        parsed_data = json.loads(data)
        
        # print("Holaaaaaaaaaaaaaaaaaaaaaaasa")
        pdf_path = generar_pdf_bloque_service(parsed_data, pdf)
        
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    
    
@app.get('/generar-pdf')
async def generar_pdf(id_proceso: int, inicio: int, fin: int, area: int, fecha: str, sede: str, aula: Optional[str] = None, pdf: Optional[str] = nombre_temporal):
    # if not pdf:
    #     pdf = "output"
    try:
        pdf_path = generar_pdf_service(id_proceso, inicio, fin, area, aula, fecha, sede, pdf)
        return FileResponse(pdf_path, media_type='application/pdf', filename=pdf_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/generar-resultados-pdf')
async def generar_resultados_pdf(id_proceso):
    try:
        pdf_resultados = generar_pdf_resultados(id_proceso)
        return FileResponse(pdf_resultados, media_type='application/pdf', filename=pdf_resultados)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/generar-constancia-bloque')
async def generar_constancia_bloque(id_proceso, tipo_documento):
    try:
        pdf_constancia = generar_constancias_por_proceso(id_proceso, tipo_documento)
        return FileResponse(pdf_constancia, media_type='application/pdf', filename=pdf_constancia)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/generar-constancia-estudiante')
async def generar_constancia_estudiante(id_proceso, dni, tipo_documento):
    try:
        pdf_constancia = generar_constancia_por_estudiante(id_proceso, dni, tipo_documento)
        return FileResponse(pdf_constancia, media_type='application/pdf', filename=pdf_constancia)
    except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get('/generar-reporte-cordinador')
async def generar_reporte_cordinador(id_proceso, dni):
    try:
        pdf_reporte = generar_reporte_por_cordinador(id_proceso, dni)
        return FileResponse(pdf_reporte, media_type='application/pdf', filename=pdf_reporte)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get('/generar-reporte-aula')
async def generar_reporte_aula(proceso, aula):
    try:
        pdf_reporte = generar_reporte_por_aula(proceso, aula)
        return FileResponse(pdf_reporte, media_type='application/pdf', filename=pdf_reporte)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))