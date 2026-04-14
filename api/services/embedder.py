import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def generar_embedding(texto: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{os.getenv('OLLAMA_URL')}/api/embeddings",
            json={"model": os.getenv("EMBED_MODEL"), "prompt": texto}
        )
        return r.json().get("embedding", [])


def chunk_texto(texto: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    palabras = texto.split()
    chunks = []
    i = 0
    while i < len(palabras):
        chunk = " ".join(palabras[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks
