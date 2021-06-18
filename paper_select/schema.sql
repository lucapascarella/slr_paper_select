DROP TABLE IF EXISTS paper;
DROP TABLE IF EXISTS remark;

CREATE TABLE paper (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  authors TEXT,
  abstract TEXT,
  venue TEXT,
  year INTEGER,
  doi TEXT,
  source TEXT
);

CREATE TABLE remark (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  paper_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author TEXT NOT NULL,
  acceptance INTEGER NOT NULL,
  inclusion_note TEXT,
  exclusion_note TEXT,
  FOREIGN KEY (paper_id) REFERENCES paper (id)
);
