from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    constructs,
    genes,
    health,
    organisms,
    optimization,
    projects,
    proteins,
    regulatory,
)


def create_app() -> FastAPI:
    application = FastAPI(
        title="GenBit API",
        description="Synthetic Biology Construct Designer",
        version="0.1.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(genes.router, prefix="/api/genes", tags=["genes"])
    application.include_router(proteins.router, prefix="/api/proteins", tags=["proteins"])
    application.include_router(organisms.router, prefix="/api/organisms", tags=["organisms"])
    application.include_router(constructs.router, prefix="/api/constructs", tags=["constructs"])
    application.include_router(
        optimization.router, prefix="/api/optimization", tags=["optimization"]
    )
    application.include_router(regulatory.router, prefix="/api/regulatory", tags=["regulatory"])
    application.include_router(projects.router, prefix="/api/projects", tags=["projects"])

    return application


app = create_app()
