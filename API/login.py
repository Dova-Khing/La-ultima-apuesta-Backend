"""
Sistema de Gestión de Juegos y Apuestas con ORM SQLAlchemy y Neon PostgreSQL
API REST con FastAPI - Sin interfaz de consola
"""

import uvicorn
from ORM.apis import auth, usuario, premio, partida, juego, boleto, historial_saldo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Gestión de Juegos y Apuestas",
    description="API REST para gestión de usuarios, apuestas y partidas con autenticación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
INCLUIR LOS ROUTERS DE LAS APIS

"""
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(premio.router)
app.include_router(partida.router)
app.include_router(juego.router)
app.include_router(boleto.router)
app.include_router(historial_saldo.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("Iniciando Sistema de Gestión de Juegos y Apuestas...")
    print("Configurando base de datos...")
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Juegos y Apuestas",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "premios": "/premios",
            "partidas": "/partidas",
            "juegos": "/juegos",
            "boletos": "/boletos",
            "historial_saldo": "/historial-saldo",
        },
    }


def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "ORM.login:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
