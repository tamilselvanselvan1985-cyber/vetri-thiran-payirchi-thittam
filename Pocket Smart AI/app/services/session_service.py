from fastapi import Request

from app.services.auth_service import (
    decode_token
)


SESSION_COOKIE = (
    "pocketsmart_token"
)


def set_session(
    response,
    token: str
):

    response.set_cookie(

        SESSION_COOKIE,

        token,

        httponly=True,

        samesite="lax",

        max_age=60 * 60 * 24
    )


def clear_session(
    response
):

    response.delete_cookie(
        SESSION_COOKIE
    )


def current_user(
    request: Request
):

    token = request.cookies.get(
        SESSION_COOKIE
    )

    if not token:

        authorization = request.headers.get(
            "Authorization",
            ""
        )

        if authorization.lower().startswith(
            "bearer "
        ):

            token = authorization[
                7:
            ].strip()

    if not token:

        return None

    try:

        return decode_token(
            token
        )

    except Exception:

        return None