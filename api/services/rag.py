import httpx
import os
from dotenv import load_dotenv
from api.db.qdrant import get_qdrant
from api.services.embedder import generar_embedding
from api.services.classifier import clasificar_pregunta

load_dotenv()

async def consultar(pregunta: str, categoria: str = None) -> dict:
    # 1. Detectar categoría si no viene especificada
    if not categoria:
        categoria = await clasificar_pregunta(pregunta)

    # 2. Generar embedding de la pregunta
    vector = await generar_embedding(pregunta)

    # 3. Buscar en Qdrant filtrando por categoría
    client = get_qdrant()
    resultados = client.search(
        collection_name=os.getenv("QDRANT_COLLECTION"),
        query_vector=vector,
        limit=4,
        query_filter={
            "must": [{"key": "categoria", "match": {"value": categoria}}]
        },
        with_payload=True
    )

    # 4. Construir contexto con los chunks encontrados
    contexto = "\n\n".join([r.payload.get("texto", "") for r in resultados])

    if not contexto.strip():
        return {
            "respuesta": f"No encontré documentos en la categoría '{categoria}' para responder tu pregunta.",
            "categoria_detectada": categoria,
            "chunks_usados": 0
        }

    # 5. Generar respuesta con Ollama
    prompt = f"""Responde la pregunta basándote ÚNICAMENTE en el contexto proporcionado.
Si el contexto no tiene suficiente información, dilo claramente.

Contexto:
{contexto}

Pregunta: {pregunta}

Respuesta:"""

    async with httpx.AsyncClient(timeout=60) as client_http:
        r = await client_http.post(
            f"{os.getenv('OLLAMA_URL')}/api/generate",
            json={"model": os.getenv("OLLAMA_MODEL"), "prompt": prompt, "stream": False}
        )
        respuesta = r.json().get("response", "No pude generar una respuesta.").strip()

    return {
        "respuesta": respuesta,
        "categoria_detectada": categoria,
        "chunks_usados": len(resultados)
    }
