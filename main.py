from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime,timedelta

from otp import generate_otp
from email_service import send_otp_email

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

from database import get_db, engine
from models import IST, Base, ChatbotUser
import schemas
print("Using schemas file:", schemas.__file__)
from schemas import UserCreate, OTPVerify

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    errors = []

    for error in exc.errors():

        field = error["loc"][-1]

        if field == "email":
            errors.append(
                "Please enter a valid email address and try again."
            )

        elif field == "name":
            errors.append(
                error["msg"]
            )

        elif field == "phone":
            errors.append(
                error["msg"]
            )

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "errors": errors
        }
    )

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "FastAPI connected to MySQL successfully"
    }


@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    print("Register API Hit")
    print(user)

    existing_user = db.query(ChatbotUser).filter(
        ChatbotUser.email == user.email
    ).first()

    if existing_user:
        return {
            "message": "Email already exists"
        }

    otp = generate_otp()

    expiry_time = datetime.now(IST) + timedelta(minutes=5)

    new_user = ChatbotUser(
        name=user.name,
        email=user.email,
        phone=user.phone,
        email_verified=False,
        otp=otp,
        otp_expiry=expiry_time
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_otp_email(
        user.email,
        otp
    )

    return {
        "success": True,
        "message": "OTP sent successfully",
        "id": new_user.id
    }


@app.post("/verify-otp")
def verify_otp(
    data: OTPVerify,
    db: Session = Depends(get_db)
):

    user = db.query(ChatbotUser).filter(
        ChatbotUser.email == data.email
    ).first()

    if not user:
        return {
            "message": "User not found"
        }

    if user.otp != data.otp:
        return {
            "message": "Invalid OTP"
        }

    if datetime.now() > user.otp_expiry:
        return {
            "message": "OTP expired"
        }

    user.email_verified = True

    db.commit()

    return {
        "message": "Email verified successfully"
    }

