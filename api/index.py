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
    ASGI entrypoint for Vercel Python runtime.
    Strips Vercel serverless function prefix from scope['path']
    so FastAPI handles the exact requested path.
    """
    if scope.get("type") in ("http", "websocket"):
        path = scope.get("path", "")
        for prefix in ("/api/index.py", "/api/index"):
            if path == prefix:
                path = "/"
                break
            elif path.startswith(prefix + "/"):
                path = path[len(prefix):]
                break
        scope["path"] = path if path else "/"

    await fastapi_app(scope, receive, send)


handler = app

