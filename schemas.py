from pydantic import BaseModel, Field

class FAQRequest(BaseModel):
    faq_id: int

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = Field(
        ...,
        min_length=1,
        max_length=300
    )


class FeedbackRequest(BaseModel):
    log_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=0, le=1)

class EndChatRequest(BaseModel):
    session_id: str


class CallbackRequest(BaseModel):
    user_id: int | None = None
    course_interest: str
    preferred_time: str
    notes: str | None = None