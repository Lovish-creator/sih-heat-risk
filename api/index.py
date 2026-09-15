"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
"""
import sys
import os
import traceback

# Resolve repository root directory and register candidate paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [root_dir, os.getcwd(), "/var/task", "/vercel/path0"]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

try:
    from backend.app.main import app
    from starlette.requests import Request
    from starlette.responses import JSONResponse
    from starlette.exceptions import HTTPException as StarletteHTTPException

    @app.middleware("http")
    async def vercel_prefix_middleware(request: Request, call_next):
        """
        Normalizes Vercel serverless function request paths.
        Vercel internal rewrites may set scope['path'] to the rewritten destination
        (/api/index.py) while preserving the original user-requested path in headers
        such as 'x-matched-path' or 'x-invoke-path'.
        """
        raw_path = request.scope.get("path", "")
        
        # Check if Vercel provided the original pre-rewrite path via headers
        matched_path = request.headers.get("x-matched-path") or request.headers.get("x-invoke-path")
        if matched_path and not matched_path.startswith("/api/index.py"):
            path = matched_path.split("?")[0]
        else:
            path = raw_path

        # Normalize serverless file prefixes
        if not path or path.strip() in ("", "/"):
            path = "/"
        elif path in ("/api", "/api/", "/api/index", "/api/index/", "/api/index.py", "/api/index.py/"):
            path = "/"
        elif path.startswith("/api/index.py/"):
            path = path[len("/api/index.py"):]
        elif path.startswith("/api/index/"):
            path = path[len("/api/index"):]

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

except Exception as startup_err:
    # Diagnostic fallback ASGI app ensuring container never crashes with FUNCTION_INVOCATION_FAILED
    from starlette.applications import Starlette
    from starlette.responses import JSONResponse
    from starlette.routing import Route

    err_trace = traceback.format_exc()

    async def _crash_handler(request):
        return JSONResponse(
            status_code=500,
            content={
                "error": "FastAPI Startup Failure",
                "detail": str(startup_err),
                "traceback": err_trace,
                "sys_path": sys.path,
                "cwd": os.getcwd(),
            }
        )

    app = Starlette(routes=[Route("/{path:path}", _crash_handler)])

# Export handler at module top-level for Vercel Python runtime
handler = app
