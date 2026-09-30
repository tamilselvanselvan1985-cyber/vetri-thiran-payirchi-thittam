import json
import uuid

from pathlib import Path

from fastapi import (
    APIRouter,
    Request,
    UploadFile,
    File,
    Form
)

from fastapi.responses import JSONResponse

from app.models.schemas import (
    HomeRequest,
    PartyRequest
)

from app.services.session_service import (
    current_user
)

from app.services.recommendation_service import (
    create_recommendation
)

from database import get_db

from config import UPLOAD_DIR


router = APIRouter()


def require_user(
    request: Request
):

    return current_user(request)


def save_history(
    user_id: int,
    planner_type: str,
    payload: dict,
    result: dict
):

    with get_db() as db:

        cursor = db.execute(
            """
            INSERT INTO recommendations
            (
                user_id,
                planner_type,
                request_json,
                response_json
            )
            VALUES (?, ?, ?, ?)
            """,

            (
                user_id,

                planner_type,

                json.dumps(
                    payload
                ),

                json.dumps(
                    result
                )
            )
        )

        return cursor.lastrowid


@router.post("/generate-home")
async def generate_home(
    data: HomeRequest,
    request: Request
):

    user = require_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Please log in first."
            },
            status_code=401
        )

    payload = data.model_dump()

    result = create_recommendation(
        "home",
        payload
    )

    recommendation_id = save_history(
        int(user["sub"]),
        "home",
        payload,
        result
    )

    return {
        "recommendation_id":
        recommendation_id,

        "planner_type":
        "home",

        **result
    }


@router.post("/generate-party")
async def generate_party(
    data: PartyRequest,
    request: Request
):

    user = require_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Please log in first."
            },
            status_code=401
        )

    payload = data.model_dump()

    result = create_recommendation(
        "party",
        payload
    )

    recommendation_id = save_history(
        int(user["sub"]),
        "party",
        payload,
        result
    )

    return {
        "recommendation_id":
        recommendation_id,

        "planner_type":
        "party",

        **result
    }


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(
        "Elegant"
    ),

    outfit_color: str = Form(
        "Any"
    ),

    notes: str = Form(
        ""
    ),

    outfit_image:
    UploadFile | None =
    File(None)
):

    user = require_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Please log in first."
            },
            status_code=401
        )

    if budget <= 0:

        return JSONResponse(
            {
                "detail":
                "Budget must be greater than zero."
            },
            status_code=422
        )

    image_path = None

    if (
        outfit_image
        and
        outfit_image.filename
    ):

        extension = Path(
            outfit_image.filename
        ).suffix.lower()

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }

        if extension not in allowed_extensions:

            return JSONResponse(
                {
                    "detail":
                    "Use JPG, PNG, or WEBP for outfit image."
                },
                status_code=400
            )

        safe_name = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        image_path = (
            UPLOAD_DIR
            / safe_name
        )

        content = await outfit_image.read()

        if len(content) > 5 * 1024 * 1024:

            return JSONResponse(
                {
                    "detail":
                    "Image must be 5 MB or smaller."
                },
                status_code=400
            )

        image_path.write_bytes(
            content
        )

    payload = {

        "budget":
        budget,

        "occasion":
        occasion.strip(),

        "style":
        style.strip(),

        "outfit_color":
        outfit_color.strip(),

        "notes":
        notes.strip(),

        "image_attached":
        bool(image_path)
    }

    result = create_recommendation(
        "jewelry",
        payload,
        image_path=image_path
    )

    recommendation_id = save_history(
        int(user["sub"]),
        "jewelry",
        payload,
        result
    )

    return {

        "recommendation_id":
        recommendation_id,

        "planner_type":
        "jewelry",

        **result
    }


@router.get(
    "/recommendations-details/{recommendation_id}"
)
def recommendation_details(
    recommendation_id: int,
    request: Request
):

    user = require_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Please log in first."
            },
            status_code=401
        )

    with get_db() as db:

        row = db.execute(
            """
            SELECT
                id,
                planner_type,
                request_json,
                response_json,
                created_at
            FROM recommendations
            WHERE id=?
            AND user_id=?
            """,

            (
                recommendation_id,
                int(user["sub"])
            )
        ).fetchone()

    if not row:

        return JSONResponse(
            {
                "detail":
                "Recommendation not found."
            },
            status_code=404
        )

    return {

        "id":
        row["id"],

        "planner_type":
        row["planner_type"],

        "request":
        json.loads(
            row["request_json"]
        ),

        "result":
        json.loads(
            row["response_json"]
        ),

        "created_at":
        row["created_at"]
    }


@router.get("/history")
def history(
    request: Request
):

    user = require_user(
        request
    )

    if not user:

        return JSONResponse(
            {
                "detail":
                "Please log in first."
            },
            status_code=401
        )

    with get_db() as db:

        rows = db.execute(
            """
            SELECT
                id,
                planner_type,
                request_json,
                response_json,
                created_at
            FROM recommendations
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 50
            """,

            (
                int(user["sub"]),
            )
        ).fetchall()

    return [

        {
            "id":
            row["id"],

            "planner_type":
            row["planner_type"],

            "request":
            json.loads(
                row["request_json"]
            ),

            "result":
            json.loads(
                row["response_json"]
            ),

            "created_at":
            row["created_at"]
        }

        for row in rows
    ]