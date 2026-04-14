# DocuMind

Sistema de gestión documental inteligente — Self-hosted.

## Qué hace
- Clasifica documentos automáticamente por categoría usando LLMs
- Indexa documentos en base de datos vectorial (Qdrant)
- Responde preguntas en lenguaje natural filtrando por categoría
- Monitorea fuentes externas y genera sugerencias proactivas
- Entrega alertas por Telegram, correo y dashboard web

## Stack
- FastAPI + Python 3.11
- Ollama (llama3.2:3b + nomic-embed-text)
- Qdrant (búsqueda vectorial)
- PostgreSQL (metadata y auditoría)
- n8n (orquestación)
- SearXNG (búsqueda externa)
- Kafka (cola de eventos)

## Infraestructura
| Servidor | IP | Rol |
|---|---|---|
| sergioserver | 100.113.116.64 | Cerebro IA + API |
| lenovoserver | 100.68.201.68 | Datos + repositorio |
| OCI ARM | 147.224.244.69 | Gateway + eventos |

## Levantar
cp .env.example .env
docker compose up -d

## API
- Swagger: http://100.113.116.64:8000/docs
- Health: http://100.113.116.64:8000/health

## Autor
Sergio Guerrero — AI Solution Architect
sergionet17@gmail.com | github.com/sergionet17
