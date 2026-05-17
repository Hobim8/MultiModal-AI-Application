from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router

load_dotenv()

app = FastAPI(
    title="YouTube query AI",
    description="Submit a YouTube video and query it in natural language without watching it.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "YouTube query AI is up and running."}
