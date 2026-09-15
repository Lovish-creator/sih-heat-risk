"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
"""
import sys
import os
import urllib.parse

# Resolve repository root directory and register candidate paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [root_dir, os.getcwd(), "/var/task", "/vercel/path0"]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

# Top-level FastAPI app export for Vercel AST static scanner
from backend.app.main import app
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

@app.middleware("http")
async def vercel_prefix_middleware(request: Request, call_next):
    """
    Normalizes Vercel serverless function request paths.
    1. If __path__ query parameter is present (passed from vercel.json rewrites),
       extract it as the true application route and strip __path__ from query_string.
    2. Otherwise, check request headers (x-matched-path, x-invoke-path) if provided.
    3. Normalize any leftover /api/index.py/ or /api/index/ prefixes.
    4. Ensure /api or /api/index.py alone routes to /api or /api/v1/health.
    """
    raw_path = request.scope.get("path", "")
    query_bytes = request.scope.get("query_string", b"")
    qs = query_bytes.decode("utf-8", errors="ignore")

    custom_path = None
    if "__path__" in qs:
        params = urllib.parse.parse_qs(qs, keep_blank_values=True)
        if "__path__" in params:
            custom_path = params.pop("__path__")[0]
            clean_qs = urllib.parse.urlencode([(k, v) for k, vs in params.items() for v in vs])
            request.scope["query_string"] = clean_qs.encode("utf-8")

    if custom_path:
        path = custom_path
    else:
        matched_path = request.headers.get("x-matched-path") or request.headers.get("x-invoke-path")
        if matched_path and not matched_path.startswith("/api/index.py"):
            path = matched_path.split("?")[0]
        else:
            path = raw_path

    # Normalize serverless file prefixes
    if path.startswith("/api/index.py/"):
        path = path[len("/api/index.py"):]
    elif path.startswith("/api/index/"):
        path = path[len("/api/index"):]
    elif path in ("/api/index.py", "/api/index"):
        path = "/api/v1/health"

    if path.startswith("/v1/"):
        path = "/api" + path

    request.scope["path"] = path
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
