"""
NIAT ParentTrust AI — FastAPI Main Application Entry Point
Autonomous Multilingual Admissions Advisory & Closer
Technology: Python FastAPI + Uvicorn + Plain HTML/CSS/JS Frontend
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.api import agent, campuses, roi, leads, webhook

app = FastAPI(
    title="NIAT ParentTrust AI",
    description="Autonomous Multilingual Admissions Advisory & Closer — NxtWave Jr. Growth Manager Project",
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for development flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(agent.router)
app.include_router(campuses.router)
app.include_router(roi.router)
app.include_router(leads.router)
app.include_router(webhook.router)


# Health check endpoints
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
def health_check():
    """System health check and diagnostic endpoint."""
    return {
        "status": "healthy",
        "service": "NIAT ParentTrust AI Engine",
        "framework": "Python FastAPI + Uvicorn",
        "frontendTechnology": "Plain HTML5 + CSS3 + Vanilla JavaScript (ES6+)",
        "backendTechnology": "Python 3.11+ / FastAPI",
        "geminiConfigured": bool(os.environ.get("GEMINI_API_KEY")),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# Mount static frontend files for seamless single-origin deployment
frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("\n" + "=" * 60)
    print(f">> NIAT ParentTrust AI Server starting at http://localhost:{port}")
    print(f"   Frontend UI:  http://localhost:{port}")
    print(f"   API Docs:     http://localhost:{port}/docs")
    print(f"   Backend:      Python FastAPI")
    print(f"   Frontend:     Plain HTML5 + CSS3 + Vanilla JavaScript")
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        print("   [+] Gemini AI: ENABLED (Live LLM responses active)")
    else:
        print("   [o] Gemini AI: STANDBY (Deterministic Multi-Tool Engine active)")
        print("       Set GEMINI_API_KEY in environment to enable live Gemini inference")
    print("=" * 60 + "\n")
    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)
