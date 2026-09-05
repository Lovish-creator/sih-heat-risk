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
    High-performance hybrid cache with In-Memory store and optional File-based persistence.
    100% resilient to read-only / serverless deployment environments (e.g. Vercel / AWS Lambda).
    """

    def __init__(self, cache_dir: str = "data/cache", default_ttl_seconds: int = 3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl_seconds
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._disk_enabled = False

        try:
            # Check if cache_dir is writable or in /tmp for serverless
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir, exist_ok=True)
            self._disk_enabled = True
        except Exception:
            # Serverless read-only environment: operate in memory
            self._disk_enabled = False

    def _get_cache_key(self, prefix: str, params: Dict[str, Any]) -> str:
        """Generate deterministic cache key from query parameters."""
        serialized = json.dumps(params, sort_keys=True)
        hash_str = hashlib.md5(serialized.encode("utf-8")).hexdigest()
        return f"{prefix}_{hash_str}"

    def get(self, prefix: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Retrieve cached payload from memory or disk if it exists and has not expired."""
        key = self._get_cache_key(prefix, params)
        now = time.time()

        # 1. Fast in-memory lookup
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if (now - entry.get("_cached_at", 0)) <= entry.get("_ttl", self.default_ttl):
                return entry.get("data")
            else:
                del self._memory_cache[key]

        # 2. Disk lookup if enabled
        if self._disk_enabled:
            filename = f"{key}.json"
            filepath = os.path.join(self.cache_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        entry = json.load(f)
                    cached_time = entry.get("_cached_at", 0)
                    ttl = entry.get("_ttl", self.default_ttl)
                    if (now - cached_time) <= ttl:
                        # Store in memory for faster subsequent lookups
                        self._memory_cache[key] = entry
                        return entry.get("data")
                except Exception:
                    pass

        return None

    def set(
        self,
        prefix: str,
        params: Dict[str, Any],
        data: Dict[str, Any],
        ttl_seconds: Optional[int] = None
    ) -> None:
        """Store payload with timestamp and TTL metadata in memory and disk."""
        key = self._get_cache_key(prefix, params)
        entry = {
            "_cached_at": time.time(),
            "_ttl": ttl_seconds or self.default_ttl,
            "_params": params,
            "data": data
        }

        # Store in memory
        self._memory_cache[key] = entry

        # Store on disk if writeable
        if self._disk_enabled:
            filename = f"{key}.json"
            filepath = os.path.join(self.cache_dir, filename)
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(entry, f, indent=2)
            except Exception:
                pass

    def count_entries(self) -> int:
        """Count total cached entries in memory and disk."""
        mem_count = len(self._memory_cache)
        if self._disk_enabled and os.path.exists(self.cache_dir):
            try:
                disk_count = len([f for f in os.listdir(self.cache_dir) if f.endswith(".json")])
                return max(mem_count, disk_count)
            except Exception:
                pass
        return mem_count
