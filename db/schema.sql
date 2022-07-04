
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dir TEXT NOT NULL,
    sym TEXT NOT NULL,
    step int NOT NULL,
    halving int NOT NULL,
    entry_price real NOT NULL,
    order_status int NOT NULL
);

-- DROP TABLE IF EXISTS posts;
-- dir, sym, step, depth, entry_price
-- CREATE TABLE symbol (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--     direction TEXT NOT NULL,
--     depth INTEGER,
--     step INTEGER NOT NULL,
--     order_status: 0 is open 1 is closed
-- );