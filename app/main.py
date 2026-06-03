from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.routes import router
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import FileResponse



load_dotenv()

app = FastAPI(
    title="YouTube query AI",
    description="Submit a YouTube video and query it in natural language without watching it.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)


@app.get("/")
def root():
    return FileResponse("static/index.html")
