from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")


class ChatbotUser(Base):

    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(20),
        nullable=False
    )

    email_verified = Column(
        Boolean,
        default=False
    )

    otp = Column(
        String(6)
    )

    otp_expiry = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
         default=lambda: datetime.now(IST)
    )

    
