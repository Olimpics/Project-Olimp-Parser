from fastapi import FastAPI
from app.api.endpoints import parser

app = FastAPI(
    title="Document Parser Microservice",
    description="Мікросервіс для парсингу документів різних форматів (Excel, PDF, Word)",
    version="0.1.0"
)

app.include_router(parser.router, prefix="/api", tags=["parser"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Document Parser Service API"}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}