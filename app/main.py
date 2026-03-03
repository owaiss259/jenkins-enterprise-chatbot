from fastapi import FastAPI, HTTPException
from app.jenkins_client import JenkinsClient

app = FastAPI()

jenkins_client = JenkinsClient()


@app.get("/health")
def health_check():
    return {"status": "Chatbot is running"}


@app.get("/jenkins/status")
def jenkins_status():
    try:
        data = jenkins_client.get_jenkins_status()

        return {
            "jenkins_name": data.get("displayName"),
            "jenkins_mode": data.get("mode"),
            "node_description": data.get("nodeDescription")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))