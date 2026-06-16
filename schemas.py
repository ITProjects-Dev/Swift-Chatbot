from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        if len(value.strip()) < 3:
            raise ValueError(
                "Please enter a valid name"
            )

        return value

    @field_validator("phone")
    @classmethod
    def validate_mobile(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Please enter your mobile number"
            )

        if value.startswith("+"):
            value = value[1:]

        if not value.isdigit():
            raise ValueError(
                "Please enter a valid mobile number"
            )

        if len(value) < 7:
            raise ValueError(
                "Mobile number is too short"
            )

        if len(value) > 15:
            raise ValueError(
                "Mobile number is too long"
            )

        return value


class OTPVerify(BaseModel):
    email: EmailStr
    otp: str