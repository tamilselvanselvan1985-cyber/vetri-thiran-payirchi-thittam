import json

from pathlib import Path

from typing import Optional

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    AI_ENABLED
)


try:

    from google import genai

    from google.genai import types

except Exception:

    genai = None

    types = None


def get_client():

    if not (
        AI_ENABLED
        and
        GEMINI_API_KEY
        and
        genai
    ):

        return None

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


def create_prompt(
    planner_type: str,
    payload: dict,
    catalog: list
):

    return f"""
You are PocketSmart AI,
a careful budget planning assistant.

Planner:
{planner_type}

User request:

{json.dumps(
    payload,
    indent=2
)}

Available local catalog candidates:

{json.dumps(
    catalog,
    indent=2
)}

Return ONLY valid JSON.

Use this structure:

{{
    "summary": "short helpful summary",

    "allocation": {{}},

    "recommendations": [
        {{
            "name": "item name",
            "category": "category",
            "estimated_price": 0,
            "quantity": 1,
            "platform": "platform",
            "reason": "short reason"
        }}
    ]
}}

Rules:

1. Keep estimated spending within the user's budget.

2. Use INR.

3. Do not claim that products are currently in stock.

4. Platform names are search destinations,
   not verified live inventory.

5. Keep explanations short.

6. For jewelry image requests,
   describe visual observations conservatively.

7. Do not invent live prices.

8. If information is missing,
   make a reasonable assumption.
"""


def generate_recommendation(
    planner_type: str,
    payload: dict,
    catalog: list,
    image_path:
    Optional[Path] = None
):

    client = get_client()

    if client is None:

        return None

    prompt = create_prompt(
        planner_type,
        payload,
        catalog
    )

    contents = [
        prompt
    ]

    if (
        image_path
        and
        image_path.exists()
        and
        types
    ):

        try:

            image_bytes = (
                image_path.read_bytes()
            )

            mime_type = "image/jpeg"

            if image_path.suffix.lower() == ".png":

                mime_type = "image/png"

            elif image_path.suffix.lower() == ".webp":

                mime_type = "image/webp"

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                )
            )

        except Exception:

            pass

    try:

        response = client.models.generate_content(

            model=GEMINI_MODEL,

            contents=contents,

            config=types.GenerateContentConfig(

                temperature=0.4,

                response_mime_type="application/json"
            )
            if types
            else None
        )

        text = (
            getattr(
                response,
                "text",
                ""
            )
            or ""
        )

        return json.loads(
            text
        )

    except Exception:

        return None