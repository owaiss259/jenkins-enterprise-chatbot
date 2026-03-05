import requests
from config import settings


def trigger_jenkins_job(job_name: str):
    try:
        session = requests.Session()
        session.auth = (settings.JENKINS_USER, settings.JENKINS_TOKEN)

        # Get CSRF crumb (if enabled)
        crumb_url = f"{settings.JENKINS_URL}/crumbIssuer/api/json"
        crumb_response = session.get(crumb_url)

        headers = {}

        if crumb_response.status_code == 200:
            crumb_data = crumb_response.json()
            headers = {
                crumb_data["crumbRequestField"]: crumb_data["crumb"]
            }

        build_url = f"{settings.JENKINS_URL}/job/{job_name}/build"

        response = session.post(build_url, headers=headers)

        print("Jenkins Status Code:", response.status_code)
        print("Jenkins Response:", response.text)

        if response.status_code in [200, 201, 202]:
            return f"Jenkins job '{job_name}' triggered successfully!"
        else:
            return f"Failed! Status: {response.status_code}"

    except Exception as e:
        return f"Error: {str(e)}"
