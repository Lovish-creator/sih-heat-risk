"""
Local File & In-Memory Response Caching System.
Prevents abusive repeated calls to public upstream APIs and ensures offline demo reliability.
"""

import json
import os
import hashlib
import time
from typing import Dict, Any, Optional


class DataCache:
    """
    Simple file-based JSON cache with Time-To-Live (TTL) expiration.
    """

    def __init__(self, cache_dir: str = "data/cache", default_ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl_seconds
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_key(self, prefix: str, params: Dict[str, Any]) -> str:
        """Generate deterministic cache filename from query parameters."""
        serialized = json.dumps(params, sort_keys=True)
        hash_str = hashlib.md5(serialized.encode("utf-8")).hexdigest()
        return f"{prefix}_{hash_str}.json"

    def get(self, prefix: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve cached payload if it exists and has not expired."""
        filename = self._get_cache_key(prefix, params)
        filepath = os.path.join(self.cache_dir, filename)

        if not os.path.exists(filepath):
            return None

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                entry = json.load(f)

            cached_time = entry.get("_cached_at", 0)
            ttl = entry.get("_ttl", self.default_ttl)

            if (time.time() - cached_time) > ttl:
                # Expired
                return None

            return entry.get("data")
        except Exception:
            return None

    def set(
        self,
        prefix: str,
        params: Dict[str, Any],
        data: Dict[str, Any],
        ttl_seconds: Optional[int] = None
    ) -> None:
        """Store payload with timestamp and TTL metadata."""
        filename = self._get_cache_key(prefix, params)
        filepath = os.path.join(self.cache_dir, filename)

        entry = {
            "_cached_at": time.time(),
            "_ttl": ttl_seconds or self.default_ttl,
            "_params": params,
            "data": data
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2)
        except Exception as e:
            # Non-blocking log
            pass

    def count_entries(self) -> int:
        """Count total files in cache directory."""
        try:
            return len([f for f in os.listdir(self.cache_dir) if f.endswith(".json")])
        except Exception:
            return 0
