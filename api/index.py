"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
"""

import sys
import os

# Add parent directory to sys.path so backend module can be resolved
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app as fastapi_app


async def app(scope, receive, send):
    """
    ASGI Proxy Wrapper for Vercel Serverless Functions.
    Strips Vercel serverless file path prefixes (/api/index.py, /api/index, /api)
    to route accurately to FastAPI endpoints and static UI assets.
    """
    if scope.get("type") in ("http", "websocket"):
        path = scope.get("path", "")
        if path.startswith("/api/index.py"):
            new_path = path[len("/api/index.py"):]
            if not new_path or not new_path.startswith("/"):
                new_path = "/" + new_path
            scope["path"] = new_path
        elif path.startswith("/api/index"):
            new_path = path[len("/api/index"):]
            if not new_path or not new_path.startswith("/"):
                new_path = "/" + new_path
            scope["path"] = new_path
        elif path == "/api":
            scope["path"] = "/"

    await fastapi_app(scope, receive, send)


# Export handler for Vercel Python runtime
handler = app
