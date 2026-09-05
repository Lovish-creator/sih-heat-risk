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


import traceback
import json

async def app(scope, receive, send):
    """
    ASGI Proxy Wrapper for Vercel Serverless Functions.
    Resolves the true requested URI from Vercel proxy headers and normalizes scope['path'].
    """
    if scope.get("type") in ("http", "websocket"):
        try:
            headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in scope.get("headers", [])}

            # Check for original path headers set by Vercel proxy
            raw_matched = (
                headers_dict.get("x-matched-path")
                or headers_dict.get("x-vercel-matched-path")
                or headers_dict.get("x-forwarded-uri")
                or headers_dict.get("x-real-path")
                or headers_dict.get("x-original-url")
                or headers_dict.get("x-rewrite-url")
            )

            if raw_matched:
                orig = raw_matched.split("?")[0]
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
        except Exception as e:
            tb = traceback.format_exc()
            error_body = json.dumps({"error": str(e), "traceback": tb}).encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"access-control-allow-origin", b"*"]
                ]
            })
            await send({
                "type": "http.response.body",
                "body": error_body
            })
    else:
        await fastapi_app(scope, receive, send)


# Export handler for Vercel Python runtime
handler = app
