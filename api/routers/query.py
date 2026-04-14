from fastapi import APIRouter
from api.models import ConsultaRequest, ConsultaResponse
from api.services.rag import consultar
from api.db.postgres import get_connection

router = APIRouter()

@router.post("/", response_model=ConsultaResponse)
async def query(request: ConsultaRequest):
    resultado = await consultar(request.pregunta, request.categoria)

    # Auditoría en PostgreSQL
    conn = await get_connection()
    await conn.execute(
        """INSERT INTO consultas (pregunta, categoria_detectada, respuesta, chunks_usados, canal)
           VALUES ($1, $2, $3, $4, $5)""",
        request.pregunta,
        resultado["categoria_detectada"],
        resultado["respuesta"],
        resultado["chunks_usados"],
        request.canal
    )
    await conn.close()

    return ConsultaResponse(**resultado)
