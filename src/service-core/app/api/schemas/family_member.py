from pydantic import BaseModel, ConfigDict, Field


class FamilyMemberCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    document_number: str | None = Field(default=None, max_length=32)
    phone: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=320)


class FamilyMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    document_number: str | None = None
    phone: str | None = None
    email: str
