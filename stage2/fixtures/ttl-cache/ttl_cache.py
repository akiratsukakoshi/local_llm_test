from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable
from typing import Generic, TypeVar


K = TypeVar("K")
V = TypeVar("V")


class TTLCache(Generic[K, V]):
    """A small LRU cache whose entries expire after a fixed TTL."""

    def __init__(self, max_size: int, ttl_seconds: float, clock: Callable[[], float]):
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        self._items: OrderedDict[K, tuple[V, float]] = OrderedDict()

    def _purge_expired(self, now: float) -> None:
        expired = [key for key, (_, expires_at) in self._items.items() if expires_at < now]
        for key in expired:
            del self._items[key]

    def set(self, key: K, value: V) -> None:
        now = self.clock()
        self._purge_expired(now)
        self._items[key] = (value, now + self.ttl_seconds)
        if len(self._items) > self.max_size:
            self._items.popitem(last=False)

    def get(self, key: K, default: V | None = None) -> V | None:
        now = self.clock()
        item = self._items.get(key)
        if item is None:
            return default
        value, expires_at = item
        if expires_at < now:
            del self._items[key]
            return default
        return value

    def __len__(self) -> int:
        self._purge_expired(self.clock())
        return len(self._items)
