"""
Food Order API - Main Application Entry Point
==============================================
FastAPI REST API application initialization, middleware setup,
router registration, static file serving, and startup lifespan management.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config.settings import settings
from app.database.base import Base
from app.database.connection import engine
import app.models

from app.routes.users import router as users_router
from app.routes.restaurants import router as restaurants_router
from app.routes.foods import router as foods_router
from app.routes.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Automatically creates all database tables on startup.
    """
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="A clean, modular RESTful Food Order API built with FastAPI and SQLAlchemy.",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)
app.include_router(restaurants_router)
app.include_router(foods_router)
app.include_router(orders_router)


frontend_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend",
    "stitch_food_delivery_web_app",
)

if os.path.isdir(frontend_dir):
    app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")


@app.get("/health", tags=["Health"], summary="Health check endpoint")
def health_check() -> dict:
    """
    Verify that the API server is running and healthy.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
    }


@app.get("/", tags=["Root"], summary="Root welcome endpoint")
def root():
    """
    Welcome endpoint redirecting directly to the frontend web app or JSON docs.
    """
    if os.path.isdir(frontend_dir):
        return RedirectResponse(url="/app/home/code.html")
    return {
        "message": f"Welcome to the {settings.APP_NAME}!",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
