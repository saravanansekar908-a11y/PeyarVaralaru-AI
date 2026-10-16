"""
PeyarVaralaru AI — FastAPI Main Application
Historical Tamil Place Name Explorer
"""
import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import init_db, SessionLocal
from app.services.seed_service import seed_database
from app.services.seed_documents import seed_research_documents
from app.services.seed_maps import seed_historical_maps
from app.services.ai_service import is_gemini_available
from app.routes import places, graph, ask, documents, districts, maps


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database, seed places, research documents, and historical maps on startup."""
    init_db()
    db = SessionLocal()
    try:
        seeded = seed_database(db)
        if seeded:
            print("[INFO] Database seeded with initial places data.")
        else:
            print("[INFO] Database already contains places data, skipping seed.")
        
        # Seed official research documents and passages
        seed_research_documents(db)

        # Seed historical archival maps and comparison observations
        seed_historical_maps(db)
    except Exception as e:
        print(f"[ERROR] Seed error: {e}")
    finally:
        db.close()

    if is_gemini_available():
        print("[INFO] Gemini AI is available.")
    else:
        print("[INFO] Gemini AI is not available. AI features will use database fallback.")

    yield


app = FastAPI(
    title="PeyarVaralaru AI",
    description="Historical Tamil Place Name Explorer — AI-Powered Research Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_origin,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(places.router)
app.include_router(graph.router)
app.include_router(ask.router)
app.include_router(documents.router)
app.include_router(districts.router)
app.include_router(maps.router)


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    db = SessionLocal()
    db_status = "connected"
    try:
        db.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )
    except Exception:
        db_status = "error"
    finally:
        db.close()

    return {
        "status": "ok",
        "database": db_status,
        "gemini_available": is_gemini_available(),
        "version": "1.0.0",
    }
