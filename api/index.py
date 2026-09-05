"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
"""

import sys
import os

# Add parent directory to sys.path so backend module can be resolved
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app

# Export app and handler for universal ASGI compatibility on Vercel
handler = app
