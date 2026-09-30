from typing import List, Literal

from pydantic import BaseModel, Field


PlannerType = Literal[
    "home",
    "party",
    "jewelry"
]


class RegisterRequest(BaseModel):

    email: str

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class HomeItem(BaseModel):

    name: str

    quantity: int = Field(
        default=1,
        ge=1,
        le=50
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    room_type: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="Modern",
        max_length=80
    )

    items: List[HomeItem] = Field(
        min_length=1,
        max_length=20
    )

    city: str = Field(
        default="Chennai",
        max_length=80
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="Flexible",
        max_length=120
    )

    city: str = Field(
        default="Chennai",
        max_length=80
    )

    preferences: str = Field(
        default="",
        max_length=500
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="Elegant",
        max_length=80
    )

    outfit_color: str = Field(
        default="Any",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=500
    )


class RecommendationResponse(BaseModel):

    recommendation_id: int

    planner_type: PlannerType

    source: str

    summary: str

    budget: float

    allocation: dict

    recommendations: list