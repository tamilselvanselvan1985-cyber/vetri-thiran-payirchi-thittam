from fastapi import APIRouter, Request

from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from app.services.session_service import (
    current_user
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


def context(
    request,
    **kwargs
):

    return {
        "request":
        request,

        "user":
        current_user(request),

        **kwargs
    }


@router.get("/")
def index(
    request: Request
):

    return templates.TemplateResponse(
        "index.html",
        context(request)
    )


@router.get("/login")
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        "login.html",
        context(request)
    )


@router.get("/register")
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        "register.html",
        context(request)
    )


@router.get("/dashboard")
def dashboard(
    request: Request
):

    if not current_user(request):

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        "dashboard.html",
        context(request)
    )


@router.get("/home-planner")
def home_planner(
    request: Request
):

    return templates.TemplateResponse(
        "home_planner.html",
        context(request)
    )


@router.get("/party-planner")
def party_planner(
    request: Request
):

    return templates.TemplateResponse(
        "party_planner.html",
        context(request)
    )


@router.get("/jewelry-planner")
def jewelry_planner(
    request: Request
):

    return templates.TemplateResponse(
        "jewelry_planner.html",
        context(request)
    )


@router.get(
    "/recommendations/{recommendation_id}"
)
def recommendations(
    request: Request,
    recommendation_id: int
):

    return templates.TemplateResponse(
        "recommendations.html",
        context(
            request,
            recommendation_id=
            recommendation_id
        )
    )


@router.get("/history")
def history_page(
    request: Request
):

    if not current_user(request):

        return RedirectResponse(
            "/login",
            status_code=303
        )

    return templates.TemplateResponse(
        "history.html",
        context(request)
    )