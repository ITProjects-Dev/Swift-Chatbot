#from fastapi import FastAPI
#from routes.chatbot import router

#app = FastAPI()

#app.include_router(router)
from fastapi import FastAPI
from routes.chatbot import router as chatbot_router
from routes.login import router as login_router
from database import Base, engine
from models import ChatbotUser

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(chatbot_router)
app.include_router(login_router)