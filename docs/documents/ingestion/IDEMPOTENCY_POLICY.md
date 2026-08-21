# Idempotency Policy
Content hashing (SHA-256) is mandatory. Unchanged hashes mean we log a `FetchEvent` but skip the `ContentVersion` creation and subsequent parsing/canonicalizing layers.
