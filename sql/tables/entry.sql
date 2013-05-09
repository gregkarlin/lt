DROP TABLE IF EXISTS entry CASCADE;

CREATE TABLE entry
(
  id                                        SERIAL PRIMARY KEY,
  author                                    VARCHAR(1000),
  buddy_icon                                VARCHAR(1000),
  static_url                                VARCHAR(10000),
  title                                     VARCHAR(10000),
  rating                                    INTEGER
);

DROP TABLE IF EXISTS entry_comments;

CREATE TABLE entry_comments
(
  id                                        SERIAL PRIMARY KEY,
  entry                                     INTEGER REFERENCES entry(id),
  comment                                   TEXT
);
