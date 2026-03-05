from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from jenkins_client import trigger_jenkins_job

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI()

# Enable CORS (so frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from .env
API_KEY = os.getenv("API_KEY")

# Serve frontend static folder
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Request model for Jenkins trigger
class JenkinsRequest(BaseModel):
    job_name: str


# Root route -> serves chatbot UI
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")


# Health check route
@app.get("/health")
def health_check():
    return {"status": "Backend Running ✅"}


# Jenkins trigger endpoint
@app.post("/jenkins/trigger")
def trigger_pipeline(
    request: JenkinsRequest,
    x_api_key: str = Header(None)
):
    # Validate API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    result = trigger_jenkins_job(request.job_name)

    return {"message": result}
