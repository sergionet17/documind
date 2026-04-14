from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from api.db.postgres import get_connection

router = APIRouter()

@router.get("/stats")
async def stats():
    conn = await get_connection()
    
    categorias = await conn.fetch(
        "SELECT categoria, COUNT(*) as total FROM documentos GROUP BY categoria ORDER BY total DESC"
    )
    recientes = await conn.fetch(
        "SELECT nombre, categoria, fuente, fecha_ingesta FROM documentos ORDER BY fecha_ingesta DESC LIMIT 10"
    )
    total_docs = await conn.fetchval("SELECT COUNT(*) FROM documentos")
    total_consultas = await conn.fetchval("SELECT COUNT(*) FROM consultas")
    total_sugerencias = await conn.fetchval("SELECT COUNT(*) FROM sugerencias WHERE leida=FALSE")
    
    await conn.close()
    
    return {
        "total_documentos": total_docs,
        "total_consultas": total_consultas,
        "sugerencias_pendientes": total_sugerencias,
        "categorias": [dict(r) for r in categorias],
        "recientes": [dict(r) for r in recientes]
    }

@router.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTMLResponse(content=open("/app/api/static/dashboard.html").read())
