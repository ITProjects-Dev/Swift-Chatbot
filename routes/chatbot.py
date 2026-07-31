from fastapi import APIRouter, HTTPException
from schemas import CourseSuggestionRequest
from services.chatbot_service import (
    get_categories,
    get_category_contents,
    get_content,
    get_content_actions,
    suggest_course,
    get_chatbot_settings,

)

router = APIRouter()

@router.get("/categories")
def categories():
    try:
        data = get_categories()

        return {
            "success": 200,
            "data": data
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/category/{category_id}")
def category_contents(category_id: int):

    try:

        data = get_category_contents(category_id)

        return {
            "success": 200,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@router.get("/content/{content_id}")
def content(content_id: int):

    try:

        chatbot_content = get_content(content_id)

        if chatbot_content is None:

            raise HTTPException(
                status_code=404,
                detail="Content not found"
            )

        actions = get_content_actions(content_id)

        return {
            "success": 200,
            "content": chatbot_content,
            "actions": actions
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/suggest-course")
def save_course_suggestion(request: CourseSuggestionRequest):

    try:

        suggest_course(
            request.suggested_course,
            request.session_id,
            request.created_by_ip
        )

        return {
            "success": 200,
            "message": "Course suggestion submitted successfully."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/settings")
def chatbot_settings():

    try:

        data = get_chatbot_settings()

        return {
            "success": 200,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )