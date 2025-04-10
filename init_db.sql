CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  message TEXT UNIQUE
);

INSERT OR IGNORE INTO messages (message) 
VALUES 
  ('Hello from SQLite!'), 
  ('Deployed with Ansible'), 
  ('Artifact stored in S3');