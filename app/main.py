from fastapi import FastAPI
from app.interfaces.api.routes import router


app = FastAPI(
    title="API de Geração de QR Codes",
    description="API para gerar QR Codes simples e com imagem central",
    version="1.0.0",
)
app.include_router(router)


def get_app():
    return app
