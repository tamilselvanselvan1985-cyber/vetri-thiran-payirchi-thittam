from fastapi import APIRouter, Request

from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)

from app.models.schemas import (
    RegisterRequest,
    LoginRequest
)

from app.services.auth_service import (
    create_user,
    authenticate,
    create_token
)

from app.services.session_service import (
    set_session,
    clear_session,
    current_user
)


router = APIRouter()


@router.post("/register")
def register(
    data: RegisterRequest
):

    user = create_user(
        data.email,
        data.password
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Email is already registered."
            },
            status_code=409
        )

    return {
        "message":
        "Registration successful",

        "user":
        user
    }


@router.post("/token")
def token(
    data: LoginRequest
):

    user = authenticate(
        data.email,
        data.password
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Invalid email or password."
            },
            status_code=401
        )

    jwt_token = create_token(
        user["id"],
        user["email"]
    )

    return {
        "access_token":
        jwt_token,

        "token_type":
        "bearer"
    }


@router.post("/login")
def login(
    data: LoginRequest
):

    user = authenticate(
        data.email,
        data.password
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Invalid email or password."
            },
            status_code=401
        )

    response = JSONResponse(
        {
            "message":
            "Login successful",

            "user": {
                "id":
                user["id"],

                "email":
                user["email"]
            }
        }
    )

    jwt_token = create_token(
        user["id"],
        user["email"]
    )

    set_session(
        response,
        jwt_token
    )

    return response


@router.get("/logout")
def logout():

    response = RedirectResponse(
        "/",
        status_code=303
    )

    clear_session(
        response
    )

    return response


@router.get("/session-info")
def session_info(
    request: Request
):

    user = current_user(
        request
    )

    return {
        "authenticated":
        bool(user),

        "user":
        user
    }


@router.get("/session-data")
def session_data(
    request: Request
):

    user = current_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Not authenticated"
            },
            status_code=401
        )

    return {
        "user_id":
        int(user["sub"]),

        "email":
        user["email"],

        "login_status":
        "active"
    }