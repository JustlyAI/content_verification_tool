"""
Document caching module for storing converted Docling documents
"""
import hashlib
import pickle
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from termcolor import cprint


# Cache directory
CACHE_DIR = Path("/tmp/document_cache")
CACHE_DIR.mkdir(exist_ok=True)

# Cache expiration time (1 hour)
CACHE_EXPIRATION = timedelta(hours=1)


class DocumentCache:
    """Simple file-based cache for Docling documents"""

    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        cprint(f"[CACHE] Initialized cache directory: {self.cache_dir}", "cyan")

    def _get_file_hash(self, file_content: bytes) -> str:
        """Generate MD5 hash of file content"""
        return hashlib.md5(file_content).hexdigest()

    def _get_cache_path(self, file_hash: str) -> Path:
        """Get cache file path for a given hash"""
        return self.cache_dir / f"{file_hash}.pkl"

    def _is_expired(self, cache_path: Path) -> bool:
        """Check if cache entry is expired"""
        if not cache_path.exists():
            return True

        # Get file modification time
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        age = datetime.now() - mtime

        return age > CACHE_EXPIRATION

    def get(self, file_content: bytes) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached document data

        Args:
            file_content: Raw file content bytes

        Returns:
            Cached data dictionary or None if not found/expired
        """
        file_hash = self._get_file_hash(file_content)
        cache_path = self._get_cache_path(file_hash)

        if cache_path.exists() and not self._is_expired(cache_path):
            try:
                with open(cache_path, "rb") as f:
                    data = pickle.load(f)
                cprint(f"[CACHE] Cache HIT for document {file_hash[:8]}...", "green")
                return data
            except Exception as e:
                cprint(f"[CACHE] Error loading cache: {e}", "red")
                # Delete corrupted cache file
                cache_path.unlink(missing_ok=True)
                return None
        else:
            cprint(f"[CACHE] Cache MISS for document {file_hash[:8]}...", "yellow")
            return None

    def set(self, file_content: bytes, data: Dict[str, Any]) -> str:
        """
        Store document data in cache

        Args:
            file_content: Raw file content bytes
            data: Data dictionary to cache

        Returns:
            File hash used as cache key
        """
        file_hash = self._get_file_hash(file_content)
        cache_path = self._get_cache_path(file_hash)

        try:
            with open(cache_path, "wb") as f:
                pickle.dump(data, f)
            cprint(f"[CACHE] Cached document {file_hash[:8]}...", "green")
            return file_hash
        except Exception as e:
            cprint(f"[CACHE] Error saving cache: {e}", "red")
            return file_hash

    def clear_expired(self):
        """Remove expired cache entries"""
        cprint("[CACHE] Clearing expired cache entries...", "cyan")
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            if self._is_expired(cache_file):
                cache_file.unlink()
                count += 1
        cprint(f"[CACHE] Removed {count} expired entries", "green")

    def clear_all(self):
        """Clear all cache entries"""
        cprint("[CACHE] Clearing all cache entries...", "cyan")
        count = 0
        for cache_file in self.cache_dir.glob("*.pkl"):
            cache_file.unlink()
            count += 1
        cprint(f"[CACHE] Removed {count} entries", "green")


# Global cache instance
document_cache = DocumentCache()
