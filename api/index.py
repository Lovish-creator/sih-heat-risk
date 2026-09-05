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


import json

async def app(scope, receive, send):
    """
    ASGI Proxy Wrapper for Vercel Serverless Functions.
    """
    if scope.get("type") in ("http", "websocket"):
        query_str = scope.get("query_string", b"").decode("latin1")
        headers_list = scope.get("headers", [])
        headers_dict = {k.decode("latin1").lower(): v.decode("latin1") for k, v in headers_list}

        # If inspect query is passed, return full diagnostic inspection of scope and environ
        if "inspect=1" in query_str or headers_dict.get("x-inspect") == "1":
            diagnostic = {
                "scope_keys": list(scope.keys()),
                "scope_path": scope.get("path"),
                "scope_raw_path": scope.get("raw_path", b"").decode("latin1", errors="ignore"),
                "scope_query_string": query_str,
                "scope_headers": headers_dict,
                "environ_keys": [k for k in os.environ.keys() if "VERCEL" in k or "PATH" in k or "URL" in k or "ROUTE" in k or "REQUEST" in k],
                "environ_vercel": {k: os.environ[k] for k in os.environ if k.startswith("VERCEL_")},
            }
            body = json.dumps(diagnostic, indent=2).encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [
                    [b"content-type", b"application/json"],
                    [b"access-control-allow-origin", b"*"]
                ],
            })
            await send({
                "type": "http.response.body",
                "body": body,
            })
            return

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
