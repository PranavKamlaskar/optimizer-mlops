import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()


JENKINS_URL = os.getenv("JENKINS_URL")
JOB_NAME = os.getenv("JENKINS_JOB")              # <-- CHANGE THIS
USER = os.getenv("JENKINS_USER")                         # <-- YOUR USERNAME
API_TOKEN = os.getenv("JENKINS_API_TOKEN")           # <-- YOUR TOKEN

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

def get_crumb():
    """Fetch Jenkins crumb for CSRF protection."""
    url = f"{JENKINS_URL}/crumbIssuer/api/json"
    resp = requests.get(url, auth=(USER, API_TOKEN))
    if resp.status_code != 200:
        print("Failed to get crumb:", resp.text)
        return {}
    data = resp.json()
    return {data["crumbRequestField"]: data["crumb"]}

def fetch_build_logs():
    crumb = get_crumb()

    # Fetch job builds list
    list_url = f"{JENKINS_URL}/job/{JOB_NAME}/api/json"
    r = requests.get(list_url, auth=(USER, API_TOKEN), headers=crumb)

    if r.status_code != 200:
        print("Error retrieving job info:", r.text)
        return

    try:
        builds = r.json().get("builds", [])
    except Exception:
        print("Could not decode JSON. Response was:")
        print(r.text)
        return

    for build in builds:
        build_number = build["number"]
        log_url = f"{JENKINS_URL}/job/{JOB_NAME}/{build_number}/consoleText"

        log_resp = requests.get(log_url, auth=(USER, API_TOKEN), headers=crumb)

        if log_resp.status_code != 200:
            print(f"Failed to retrieve log for build #{build_number}")
            continue

        log_text = log_resp.text
        filename = f"{RAW_DIR}/jenkins_{JOB_NAME}_{build_number}.log"

        with open(filename, "w") as f:
            f.write(log_text)

        print(f"Saved: {filename}")

if __name__ == "__main__":
    fetch_build_logs()

