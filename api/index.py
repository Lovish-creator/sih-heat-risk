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
    Extracts the original requested path from Vercel proxy headers
    (x-matched-path, x-vercel-matched-path, etc.) and restores it in scope['path']
    so FastAPI routers and static file handlers match the exact requested URI.
    """
    if scope.get("type") in ("http", "websocket"):
        headers_dict = dict(scope.get("headers", []))

        # Check for original path headers set by Vercel proxy
        raw_matched = (
            headers_dict.get(b"x-matched-path")
            or headers_dict.get(b"x-vercel-matched-path")
            or headers_dict.get(b"x-forwarded-uri")
            or headers_dict.get(b"x-real-path")
            or headers_dict.get(b"x-original-url")
            or headers_dict.get(b"x-rewrite-url")
        )

        if raw_matched:
            orig = raw_matched.decode("utf-8", errors="ignore").split("?")[0]
            if orig in ("/api/index.py", "/api/index", "/api"):
                scope["path"] = "/"
            elif orig:
                scope["path"] = orig
        else:
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

    await fastapi_app(scope, receive, send)


# Export handler for Vercel Python runtime
handler = app
