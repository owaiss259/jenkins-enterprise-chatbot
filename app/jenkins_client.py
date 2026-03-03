import requests
from requests.auth import HTTPBasicAuth
from app.config import settings


class JenkinsClient:

    def __init__(self):
        if not settings.JENKINS_URL:
            raise ValueError("JENKINS_URL not configured")

        self.base_url = settings.JENKINS_URL
        self.auth = HTTPBasicAuth(
            settings.JENKINS_USERNAME,
            settings.JENKINS_API_TOKEN
        )

    def get_jenkins_status(self):
        """
        Simple health check: fetch Jenkins info
        """
        url = f"{self.base_url}/api/json"

        response = requests.get(url, auth=self.auth, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to connect to Jenkins: {response.status_code}")

        return response.json()