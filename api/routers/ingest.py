from fastapi import APIRouter, UploadFile, File, Form
from api.services.classifier import clasificar_documento
from api.services.embedder import generar_embedding, chunk_texto
from api.db.postgres import get_connection
from api.db.qdrant import get_qdrant
import os, uuid
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

@router.post("/")
async def ingest(
    nombre: str = Form(...),
    fuente: str = Form(default="api"),
    file: UploadFile = File(...)
):
    # 1. Leer contenido
    contenido = (await file.read()).decode("utf-8", errors="ignore")

    # 2. Clasificar categoría
    categoria = await clasificar_documento(contenido)

    # 3. Chunkear y generar embeddings
    chunks = chunk_texto(contenido)
    qdrant = get_qdrant()
    puntos = []

    for chunk in chunks:
        vector = await generar_embedding(chunk)
        puntos.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "texto": chunk,
                "categoria": categoria,
                "nombre_documento": nombre,
                "fuente": fuente
            }
        })

    # 4. Indexar en Qdrant
    from qdrant_client.models import PointStruct
    qdrant.upsert(
        collection_name=os.getenv("QDRANT_COLLECTION"),
        points=[PointStruct(**p) for p in puntos]
    )

    # 5. Registrar en PostgreSQL
    conn = await get_connection()
    await conn.execute(
        """INSERT INTO documentos (nombre, categoria, fuente, metadata)
           VALUES ($1, $2, $3, $4)""",
        nombre, categoria, fuente,
        f'{{"chunks": {len(chunks)}}}'
    )
    await conn.close()

    return {
        "mensaje": "Documento indexado correctamente",
        "nombre": nombre,
        "categoria": categoria,
        "chunks": len(chunks)
    }
