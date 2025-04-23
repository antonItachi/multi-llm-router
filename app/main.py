from fastapi import FastAPI
from app.logger import configure_logger
import app.router as router

app = FastAPI()

app.include_router(router.router)

configure_logger()

@app.get("/")
def root():
    return {"message": "RAG Voting API is running"}