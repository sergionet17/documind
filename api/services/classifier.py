import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CATEGORIAS = [
    "arquitectura", "tecnologia", "legal", "financiero",
    "regulacion", "rrhh", "operaciones", "otro"
]

EJEMPLOS = """
- "cómo funcionan los microservicios" → tecnologia
- "política de arquitectura de software" → arquitectura
- "contrato de trabajo empleado" → legal
- "balance financiero del trimestre" → financiero
- "norma ISO 27001 cumplimiento" → regulacion
- "vacaciones y permisos empleados" → rrhh
- "proceso de facturación clientes" → operaciones
"""

async def _llamar_ollama(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            f"{os.getenv('OLLAMA_URL')}/api/generate",
            json={"model": os.getenv("OLLAMA_MODEL"), "prompt": prompt, "stream": False}
        )
        resultado = r.json().get("response", "otro").strip().lower()
        # Extraer solo la primera palabra
        primera = resultado.split()[0].rstrip(".,:")
        return primera if primera in CATEGORIAS else "otro"


async def clasificar_documento(texto: str) -> str:
    prompt = f"""Eres un clasificador de documentos empresariales.
Analiza el texto y responde ÚNICAMENTE con UNA palabra de las categorías válidas.

Categorías válidas: {", ".join(CATEGORIAS)}

Ejemplos:
{EJEMPLOS}

Texto a clasificar:
{texto[:1000]}

Responde solo con la categoría:"""
    return await _llamar_ollama(prompt)


async def clasificar_pregunta(pregunta: str) -> str:
    prompt = f"""Eres un clasificador de preguntas empresariales.
Identifica el tema de la pregunta y responde ÚNICAMENTE con UNA palabra de las categorías válidas.

Categorías válidas: {", ".join(CATEGORIAS)}

Ejemplos:
{EJEMPLOS}

Pregunta a clasificar: {pregunta}

Responde solo con la categoría:"""
    return await _llamar_ollama(prompt)
