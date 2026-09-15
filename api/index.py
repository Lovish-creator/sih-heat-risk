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
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.middleware("http")
async def vercel_prefix_middleware(request: Request, call_next):
    """
    Strips Vercel serverless function prefix from scope['path']
    so FastAPI routes match regardless of rewrite format.
    """
    path = request.scope.get("path", "")
    if not path or path.strip() in ("", "/"):
        request.scope["path"] = "/"
    elif path in ("/api", "/api/", "/api/index", "/api/index/", "/api/index.py", "/api/index.py/"):
        request.scope["path"] = "/"
    elif path.startswith("/api/index.py/"):
        request.scope["path"] = path[len("/api/index.py"):]
    elif path.startswith("/api/index/"):
        request.scope["path"] = path[len("/api/index"):]

    return await call_next(request)

@app.exception_handler(404)
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Not Found",
                "debug": {
                    "method": request.method,
                    "url": str(request.url),
                    "url_path": request.url.path,
                    "scope_path": request.scope.get("path"),
                    "scope_root_path": request.scope.get("root_path"),
                    "raw_path": request.scope.get("raw_path", b"").decode("utf-8", errors="ignore"),
                    "headers": dict(request.headers),
                }
            }
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Export handler at module top-level for Vercel Python runtime
handler = app


