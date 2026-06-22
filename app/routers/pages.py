import logging
from fastapi import APIRouter, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db
from app.models import ContactSubmission
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    """Serve the main landing page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/admin", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Admin login page."""
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/admin", response_class=HTMLResponse)
async def admin_login(
    request: Request,
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle admin login form submission."""
    if password != settings.ADMIN_PASSWORD:
        return templates.TemplateResponse(
            "admin_login.html",
            {"request": request, "error": "Invalid password. Please try again."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    # Fetch leads for the dashboard
    leads = db.query(ContactSubmission).order_by(desc(ContactSubmission.created_at)).all()
    total = len(leads)
    unread = sum(1 for l in leads if not l.is_read)

    # Mark all as read
    db.query(ContactSubmission).filter(ContactSubmission.is_read == False).update({"is_read": True})
    db.commit()

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "leads": leads,
            "total": total,
            "unread": unread,
        }
    )


@router.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    token: str = "",
    db: Session = Depends(get_db),
):
    """Admin dashboard — requires ?token= query param matching ADMIN_PASSWORD."""
    if token != settings.ADMIN_PASSWORD:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    leads = db.query(ContactSubmission).order_by(desc(ContactSubmission.created_at)).all()
    total = len(leads)
    unread = sum(1 for l in leads if not l.is_read)

    db.query(ContactSubmission).filter(ContactSubmission.is_read == False).update({"is_read": True})
    db.commit()

    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "leads": leads, "total": total, "unread": unread}
    )
