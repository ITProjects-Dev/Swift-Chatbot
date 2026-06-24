from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()

password = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER')}:"
    f"{password}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)