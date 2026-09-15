"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
"""
import sys
import os

# Resolve repository root directory and register candidate paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [root_dir, os.getcwd(), "/var/task", "/vercel/path0"]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

from backend.app.main import app

@app.middleware("http")
async def vercel_prefix_middleware(request, call_next):
    """
    Strips Vercel serverless function prefix from scope['path']
    so FastAPI routes match regardless of rewrite format.
    """
    path = request.scope.get("path", "")
    for prefix in ("/api/index.py", "/api/index"):
        if path == prefix:
            request.scope["path"] = "/"
            break
        elif path.startswith(prefix + "/"):
            request.scope["path"] = path[len(prefix):]
            break
    return await call_next(request)

# Export handler at module top-level for Vercel Python runtime
handler = app


