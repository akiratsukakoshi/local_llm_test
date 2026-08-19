import unittest

from ttl_cache import TTLCache


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class TTLCacheTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()

    def test_rejects_non_positive_limits(self):
        with self.assertRaises(ValueError):
            TTLCache(0, 5, self.clock)
        with self.assertRaises(ValueError):
            TTLCache(2, 0, self.clock)

    def test_returns_values_and_missing_default(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("missing", 99), 99)

    def test_value_is_live_before_expiry(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        self.clock.advance(4.999)
        self.assertEqual(cache.get("a"), 1)

    def test_value_expires_at_exact_boundary(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        self.clock.advance(5)
        self.assertIsNone(cache.get("a"))

    def test_len_purges_entries_at_expiry_boundary(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        self.clock.advance(5)
        self.assertEqual(len(cache), 0)

    def test_successful_get_refreshes_lru_order(self):
        cache = TTLCache(2, 10, self.clock)
        cache.set("a", 1)
        cache.set("b", 2)
        self.assertEqual(cache.get("a"), 1)
        cache.set("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertIsNone(cache.get("b"))
        self.assertEqual(cache.get("c"), 3)

    def test_updating_key_refreshes_lru_order_and_ttl(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        cache.set("b", 2)
        self.clock.advance(2)
        cache.set("a", 10)
        cache.set("c", 3)
        self.assertEqual(cache.get("a"), 10)
        self.assertIsNone(cache.get("b"))
        self.clock.advance(3)
        self.assertEqual(cache.get("a"), 10)

    def test_expired_entries_are_removed_before_capacity_eviction(self):
        cache = TTLCache(2, 5, self.clock)
        cache.set("a", 1)
        self.clock.advance(3)
        cache.set("b", 2)
        self.clock.advance(2)
        cache.set("c", 3)
        self.assertIsNone(cache.get("a"))
        self.assertEqual(cache.get("b"), 2)
        self.assertEqual(cache.get("c"), 3)


if __name__ == "__main__":
    unittest.main()
