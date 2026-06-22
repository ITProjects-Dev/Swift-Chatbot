from fastapi import FastAPI
from routes.chatbot import router

app = FastAPI()

app.include_router(router)