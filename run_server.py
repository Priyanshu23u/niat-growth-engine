"""
NIAT ParentTrust AI — Development & Production Server Launcher
Usage:
    python run_server.py
"""

import os
import sys
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project root is in python path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Try loading .env if available
env_file = project_root / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=env_file)
    except ImportError:
        pass

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    print("\n" + "=" * 60)
    print(">> Starting NIAT ParentTrust AI Server")
    print(f"   Frontend UI:  http://localhost:{port}")
    print(f"   API Docs:     http://localhost:{port}/docs")
    print(f"   Health Check: http://localhost:{port}/health")
    print(f"   Technology:   Python FastAPI + Plain HTML5/CSS3/Vanilla JS")
    groq_key = os.environ.get("GROQ_API_KEY")
    groq_model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    if groq_key:
        print(f"   [+] Groq AI: ENABLED (Live LLM: {groq_model})")
    else:
        print("   [o] Groq AI: STANDBY (Deterministic Multi-Tool Engine active)")
        print("       Set GROQ_API_KEY in environment or .env to activate live Groq inference")
    print("=" * 60 + "\n")

    uvicorn.run("backend.app.main:app", host=host, port=port, reload=False)
