from sqlalchemy import text
from database import engine


def get_categories():
    query = text("""
        SELECT
            category_id,
            category_name,
            category_icon
        FROM chat_categories
        WHERE status = 1
        ORDER BY display_order
    """)

    with engine.connect() as connection:
        result = connection.execute(query)

        categories = []

        for row in result:
            categories.append({
                "category_id": row.category_id,
                "category_name": row.category_name,
                "category_icon": row.category_icon
            })

        return categories


def get_category_contents(category_id):
    query = text("""
        SELECT
            content_id,
            title,
            content_type
        FROM chat_contents
        WHERE category_id = :category_id
        AND parent_content_id IS NULL
        AND status = 1
        ORDER BY display_order
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "category_id": category_id
            }
        )

        contents = []

        for row in result:
            contents.append({
                "content_id": row.content_id,
                "title": row.title,
                "content_type": row.content_type
            })

        return contents


def get_content(content_id):
    query = text("""
        SELECT
            content_id,
            title,
            content
        FROM chat_contents
        WHERE content_id = :content_id
        AND status = 1
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "content_id": content_id
            }
        ).fetchone()

        if result is None:
            return None

        return {
            "content_id": result.content_id,
            "title": result.title,
            "content": result.content
        }

def get_content_actions(content_id):
    query = text("""
        SELECT
            action_id,
            action_label,
            action_type,
            action_value
        FROM chat_actions
        WHERE content_id = :content_id
        AND status = 1
        ORDER BY display_order
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "content_id": content_id
            }
        )

        actions = []

        for row in result:

            actions.append({
                "action_id": row.action_id,
                "action_label": row.action_label,
                "action_type": row.action_type,
                "action_value": row.action_value
            })

        return actions

def suggest_course(suggested_course, session_id=None, created_by_ip=None):

    query = text("""
        INSERT INTO course_suggestions
        (
            suggested_course,
            session_id,
            created_by_ip
        )
        VALUES
        (
            :suggested_course,
            :session_id,
            :created_by_ip
        )
    """)

    with engine.begin() as connection:

        connection.execute(
            query,
            {
                "suggested_course": suggested_course,
                "session_id": session_id,
                "created_by_ip": created_by_ip
            }
        )

    return True


def get_chatbot_settings():

    query = text("""
        SELECT
            setting_key,
            setting_value
        FROM chatbot_settings
    """)

    with engine.connect() as connection:

        result = connection.execute(query)

        settings = {}

        for row in result:
            settings[row.setting_key] = row.setting_value

        return settings