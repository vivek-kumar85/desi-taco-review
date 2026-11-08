-- One row per review the page has ever shown: its fingerprint and when.
CREATE TABLE IF NOT EXISTS seen (
  h  TEXT PRIMARY KEY,  -- SHA-256 of the review's words (lowercase, no punctuation or emoji)
  at INTEGER NOT NULL   -- when it was first shown (milliseconds since 1970)
);
