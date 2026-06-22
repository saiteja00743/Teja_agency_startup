import logging
import threading
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ContactSubmission
from app.schemas import (
    ContactFormRequest,
    ContactFormResponse,
    LeadsListResponse,
    LeadOut,
    HealthResponse,
)
from app.email_utils import send_lead_notification
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api", tags=["API"])


# ── Health Check ─────────────────────────────────────────────────────────────

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check for uptime monitors (UptimeRobot, Railway, etc.)."""
    try:
        db.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return HealthResponse(
        status="ok",
        app=settings.APP_NAME,
        environment=settings.APP_ENV,
        db=db_status,
    )


# ── Contact Form ─────────────────────────────────────────────────────────────

@router.post("/contact", response_model=ContactFormResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact(
    payload: ContactFormRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Save a contact form submission to the database and trigger an email notification.
    """
    # Get client IP for basic spam tracking
    ip = request.client.host if request.client else None
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()

    # Persist the lead
    submission = ContactSubmission(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        service=payload.service,
        budget=payload.budget,
        message=payload.message,
        ip_address=ip,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    logger.info(f"New lead saved: id={submission.id} email={submission.email}")

    # Send email notification in background (non-blocking)
    thread = threading.Thread(
        target=send_lead_notification,
        args=(
            payload.name,
            payload.email,
            payload.phone or "",
            payload.service or "",
            payload.budget or "",
            payload.message,
        ),
        daemon=True,
    )
    thread.start()

    return ContactFormResponse(
        success=True,
        message="Thanks! We'll be in touch within 24 hours.",
        id=submission.id,
    )


# ── Admin Leads API ──────────────────────────────────────────────────────────

@router.get("/leads", response_model=LeadsListResponse)
async def list_leads(
    request: Request,
    token: str = "",
    db: Session = Depends(get_db),
):
    """
    Return all leads as JSON. Requires ?token=<ADMIN_PASSWORD>.
    Used by the admin dashboard frontend.
    """
    if token != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    leads = db.query(ContactSubmission).order_by(ContactSubmission.created_at.desc()).all()
    unread = sum(1 for l in leads if not l.is_read)

    return LeadsListResponse(
        total=len(leads),
        unread=unread,
        leads=[LeadOut.model_validate(l) for l in leads],
    )


@router.delete("/leads/{lead_id}")
async def delete_lead(
    lead_id: int,
    token: str = "",
    db: Session = Depends(get_db),
):
    """Delete a specific lead. Requires ?token=<ADMIN_PASSWORD>."""
    if token != settings.ADMIN_PASSWORD:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    lead = db.query(ContactSubmission).filter(ContactSubmission.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

    db.delete(lead)
    db.commit()
    return {"success": True, "message": f"Lead {lead_id} deleted"}
