import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    JENKINS_URL = os.getenv("JENKINS_URL")
    JENKINS_USERNAME = os.getenv("JENKINS_USERNAME")
    JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")

settings = Settings()