import sqlite3

from contextlib import contextmanager
from pathlib import Path

from config import DATABASE_PATH


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    planner_type TEXT NOT NULL,

    request_json TEXT NOT NULL,

    response_json TEXT NOT NULL,

    created_at TEXT NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
);
"""


@contextmanager
def get_db():

    Path(DATABASE_PATH).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    try:

        yield connection

        connection.commit()

    finally:

        connection.close()


def init_db():

    with get_db() as connection:

        connection.executescript(
            SCHEMA
        )