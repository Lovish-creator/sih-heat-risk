"""
Vercel Serverless Entrypoint for SIH26083 FastAPI Application.
Resilient to serverless path rewriting, read-only environments, and import anomalies.
"""
import sys
import os
import traceback

# Resolve repository root directory and register candidate paths
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for p in [root_dir, os.getcwd(), "/var/task", "/vercel/path0"]:
    if p and os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

import_error = None
try:
    from backend.app.main import app as real_app
except Exception:
    import_error = traceback.format_exc()
    real_app = None

if import_error is not None:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI(title="SIH26083 Diagnostic Handler")

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"])
    async def diagnostic_catch_all(full_path: str = ""):
        return JSONResponse(
            status_code=200,
            content={
                "status": "startup_import_failed",
                "error": import_error,
                "sys_path": sys.path,
                "cwd": os.getcwd(),
                "cwd_items": os.listdir(os.getcwd()) if os.path.exists(os.getcwd()) else [],
                "root_items": os.listdir(root_dir) if os.path.exists(root_dir) else [],
            }
        )
else:
    app = real_app

    @app.middleware("http")
    async def normalize_vercel_path(request, call_next):
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

        try:
            return await call_next(request)
        except Exception as exc:
            import traceback
            from starlette.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error in Vercel Runtime",
                    "details": str(exc),
                    "traceback": traceback.format_exc()
                }
            )

    @app.get("/api/diagnostic", include_in_schema=False)
    async def diagnostic_route():
        """Lightweight diagnostic endpoint for deployment verification."""
        return {
            "status": "ok",
            "cwd": os.getcwd(),
            "sys_path": sys.path[:6],
            "backend_loaded": True,
            "frontend_exists": os.path.exists(os.path.join(os.getcwd(), "frontend")),
        }

# Aliased for Vercel Python runtime
handler = app


