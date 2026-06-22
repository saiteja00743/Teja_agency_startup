from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


# ── Contact Form ─────────────────────────────────────────────────────────────

class ContactFormRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service: Optional[str] = None
    budget: Optional[str] = None
    message: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        if len(v) > 100:
            raise ValueError("Name must be under 100 characters")
        return v

    @field_validator("message")
    @classmethod
    def message_must_not_be_empty(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("Message must be at least 10 characters")
        if len(v) > 5000:
            raise ValueError("Message must be under 5000 characters")
        return v


class ContactFormResponse(BaseModel):
    success: bool
    message: str
    id: Optional[int] = None


# ── Admin Lead View ──────────────────────────────────────────────────────────

class LeadOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    service: Optional[str]
    budget: Optional[str]
    message: str
    is_read: bool
    ip_address: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class LeadsListResponse(BaseModel):
    total: int
    unread: int
    leads: list[LeadOut]


# ── Health Check ─────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
    db: str
