from fastapi import FastAPI
from api.routers import ingest, query, scraper, suggestions

app = FastAPI(
    title="DocuMind API",
    description="Sistema de gestión documental inteligente - Self-hosted",
    version="1.0.0"
)

app.include_router(ingest.router,       prefix="/ingest",      tags=["Ingesta"])
app.include_router(query.router,        prefix="/query",       tags=["Consulta"])
app.include_router(scraper.router,      prefix="/scrape",      tags=["Scraping"])
app.include_router(suggestions.router,  prefix="/suggestions", tags=["Sugerencias"])

@app.get("/health")
async def health():
    return {"status": "ok", "sistema": "DocuMind v1.0"}
