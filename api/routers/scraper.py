from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def scraper_placeholder():
    return {"mensaje": "Módulo de scraping - próximamente Sprint 3"}
