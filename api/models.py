from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentoIngesta(BaseModel):
    nombre: str
    contenido: str
    fuente: str = "api"

class ConsultaRequest(BaseModel):
    pregunta: str
    categoria: Optional[str] = None
    canal: str = "api"

class ConsultaResponse(BaseModel):
    respuesta: str
    categoria_detectada: str
    chunks_usados: int

class SugerenciaResponse(BaseModel):
    id: int
    fuente: str
    categoria: str
    titulo: str
    texto: str
    url: Optional[str]
    fecha_generacion: datetime
    leida: bool
