from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class MenuNodeDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    path: str
    label: str
    icon: str | None = None
    sort_order: int = 0
    children: list["MenuNodeDto"] = []


class UserSummaryDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str
    roles: list[str]


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSummaryDto
    menu: list[MenuNodeDto]


class MeResponse(BaseModel):
    user: UserSummaryDto
    menu: list[MenuNodeDto]


class CreateVolunteerRequest(BaseModel):
    email: str
    password: str
    full_name: str


class CreateVolunteerResponse(BaseModel):
    id: int
    email: str
    full_name: str
    roles: list[str]
