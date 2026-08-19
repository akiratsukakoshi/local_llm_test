# TTLCache debugging fixture

This is the first unfamiliar single-file debugging fixture after the slugify smoke and compatibility suites.

The initial implementation intentionally has four failing tests out of eight:

- expiry at the exact TTL boundary through `get`;
- expiry at the exact TTL boundary through `len`;
- successful reads refreshing LRU order;
- updates refreshing LRU order while resetting TTL.

The implementation file is editable and the test file is read-only. Python caches are ignored so approved tests cannot create tracked binary changes.

Run `ttl-cache-control.json` and `ttl-cache-autonomous.json` on independent clean workspaces. Hold the model, runtime, adapter, endpoint, acceptance criteria, attempt limit, and protected tests constant; only the behavioral rule packet changes.
