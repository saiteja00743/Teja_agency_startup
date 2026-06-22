from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ContactSubmission(Base):
    """Stores every contact form submission from the landing page."""
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    service = Column(String(100), nullable=True)   # Which service they're interested in
    budget = Column(String(50), nullable=True)      # Budget range
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String(50), nullable=True)  # For spam protection
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<ContactSubmission id={self.id} email={self.email}>"
