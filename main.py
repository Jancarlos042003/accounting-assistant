from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers.document import documents_router

load_dotenv()
app = FastAPI()

app.include_router(documents_router, prefix="/documents")
