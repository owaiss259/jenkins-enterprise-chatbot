import requests
from requests.auth import HTTPBasicAuth
from config import JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN

def get_crumb():
    try:
        crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
        response = requests.get(
            crumb_url,
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN)
        )

        if response.status_code == 200:
            data = response.json()
            return {data["crumbRequestField"]: data["crumb"]}
        else:
            print("Crumb fetch failed:", response.text)
            return {}

    except Exception as e:
        print("Crumb error:", str(e))
        return {}


def trigger_jenkins_job(job_name):
    try:
        url = f"{JENKINS_URL}/job/{job_name}/build"

        headers = get_crumb()

        response = requests.post(
            url,
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_API_TOKEN),
            headers=headers
        )

        print("Triggering URL:", url)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)

        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "message": f"Jenkins job '{job_name}' triggered successfully"
            }
        else:
            return {
                "status": "error",
                "message": f"Failed! Status: {response.status_code}"
            }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
