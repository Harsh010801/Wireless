"""FastAPI application entry point for Wireless Signal Propagation Analysis."""

import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(ROOT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / "src"))

from backend.routes.simulation import router as simulation_router

app = FastAPI(
    title="Wireless Signal Propagation Analysis API",
    description="REST API wrapping src/propagation/ models for React frontend consumption.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation_router)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "project": "Comparative Analysis of Wireless Signal Propagation Models",
        "course": "21CSE458T — Wireless and Mobile Communication",
        "team": [
            {"name": "Harsh Yadav", "reg_no": "RA2311003011546"},
            {"name": "Utkarsh Dabas", "reg_no": "RA2311003011550"},
            {"name": "Tamanna Singh", "reg_no": "RA2311003011570"},
        ],
    }
