from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml_model.hybrid import hybrid_analyze

app = FastAPI(
    title="Phishing Email Detector API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Later, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmailRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {
        "message": "Phishing Email Detector API is running"
    }


@app.post("/analyze-hybrid")
def analyze(request: EmailRequest):
    return hybrid_analyze(request.text)