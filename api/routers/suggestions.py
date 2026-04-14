from fastapi import APIRouter, Query
from api.db.postgres import get_connection

router = APIRouter()

@router.get("/")
async def listar_sugerencias(
    categoria: str = Query(default=None),
    leida: bool = Query(default=False)
):
    conn = await get_connection()
    if categoria:
        rows = await conn.fetch(
            "SELECT * FROM sugerencias WHERE categoria=$1 AND leida=$2 ORDER BY fecha_generacion DESC LIMIT 20",
            categoria, leida
        )
    else:
        rows = await conn.fetch(
            "SELECT * FROM sugerencias WHERE leida=$1 ORDER BY fecha_generacion DESC LIMIT 20",
            leida
        )
    await conn.close()
    return [dict(r) for r in rows]

@router.patch("/{id}/leida")
async def marcar_leida(id: int):
    conn = await get_connection()
    await conn.execute("UPDATE sugerencias SET leida=TRUE WHERE id=$1", id)
    await conn.close()
    return {"mensaje": f"Sugerencia {id} marcada como leída"}
