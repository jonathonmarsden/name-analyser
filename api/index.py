"""
Vercel serverless function entry point for FastAPI.
"""

import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Import the FastAPI app
from api.main import app
from mangum import Mangum

# Wrap FastAPI with Mangum for serverless compatibility
handler = Mangum(app, lifespan="off")
