import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_KEY = os.getenv("API_KEY")
    JENKINS_URL = os.getenv("JENKINS_URL")
    JENKINS_USER = os.getenv("JENKINS_USER")
    JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")


settings = Settings()
