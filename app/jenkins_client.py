import requests
from requests.auth import HTTPBasicAuth
from app.config import settings


class JenkinsClient:

    def __init__(self):
        if not settings.JENKINS_URL:
            raise ValueError("JENKINS_URL not configured")

        if not settings.JENKINS_USERNAME:
            raise ValueError("JENKINS_USERNAME not configured")

        if not settings.JENKINS_API_TOKEN:
            raise ValueError("JENKINS_API_TOKEN not configured")

        self.base_url = settings.JENKINS_URL.rstrip("/")
        self.auth = HTTPBasicAuth(
            settings.JENKINS_USERNAME,
            settings.JENKINS_API_TOKEN
        )

    def get_jenkins_status(self):
        """
        Fetch Jenkins system information
        """
        url = f"{self.base_url}/api/json"

        response = requests.get(url, auth=self.auth, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to connect to Jenkins: {response.status_code}")

        return response.json()

    def trigger_job(self, job_name: str):
        """
        Trigger a Jenkins job by name
        """
        if not job_name:
            raise ValueError("Job name is required")

        url = f"{self.base_url}/job/{job_name}/build"

        response = requests.post(url, auth=self.auth, timeout=10)

        if response.status_code not in [200, 201, 202]:
            raise Exception(f"Failed to trigger job: {response.status_code}")

        return {"message": f"Job '{job_name}' triggered successfully"}