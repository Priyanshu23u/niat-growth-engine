"""
Vercel Serverless Entrypoint for NIAT ParentTrust AI FastAPI Application
"""
import sys
from pathlib import Path

# Add project root to sys.path so 'backend' is importable by Vercel's Python runtime
root = Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from backend.app.main import app
