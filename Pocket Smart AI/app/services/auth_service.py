from datetime import (
    datetime,
    timedelta,
    timezone
)

import jwt

from pwdlib import PasswordHash

from config import SECRET_KEY

from database import get_db


password_hash = PasswordHash.recommended()


ALGORITHM = "HS256"


TOKEN_MINUTES = 60 * 24


def hash_password(
    password: str
):

    return password_hash.hash(
        password
    )


def verify_password(
    password: str,
    hashed: str
):

    return password_hash.verify(
        password,
        hashed
    )


def create_user(
    email: str,
    password: str
):

    email = email.strip().lower()

    with get_db() as db:

        existing = db.execute(
            """
            SELECT id
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        if existing:

            return None

        cursor = db.execute(
            """
            INSERT INTO users
            (
                email,
                password_hash
            )
            VALUES (?, ?)
            """,

            (
                email,
                hash_password(password)
            )
        )

        return {

            "id":
            cursor.lastrowid,

            "email":
            email
        }


def authenticate(
    email: str,
    password: str
):

    email = email.strip().lower()

    with get_db() as db:

        row = db.execute(
            """
            SELECT
                id,
                email,
                password_hash,
                created_at
            FROM users
            WHERE email=?
            """,

            (email,)
        ).fetchone()

    if not row:

        return None

    if not verify_password(
        password,
        row["password_hash"]
    ):

        return None

    return dict(row)


def create_token(
    user_id: int,
    email: str
):

    now = datetime.now(
        timezone.utc
    )

    payload = {

        "sub":
        str(user_id),

        "email":
        email,

        "iat":
        now,

        "exp":
        now +
        timedelta(
            minutes=TOKEN_MINUTES
        )
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(
    token: str
):

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[
            ALGORITHM
        ]
    )