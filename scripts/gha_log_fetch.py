import os
import requests
import zipfile
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

GH_TOKEN = os.getenv("GH_TOKEN")
OWNER = os.getenv("OWNER")
REPO = os.getenv("REPO")
RAW_DIR = "data/raw"

def fetch_gha_logs():
    if not GH_TOKEN or not OWNER or not REPO:
        raise ValueError("GH_TOKEN, OWNER, and REPO must be set in your .env file")

    os.makedirs(RAW_DIR, exist_ok=True)

    runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    resp = requests.get(runs_url, headers=headers)
    if resp.status_code != 200:
        print("Error fetching runs:")
        print("Status:", resp.status_code)
        print("Body:", resp.text)
        return

    runs = resp.json()

    # Debug: show keys so we know what we got
    print("Response keys:", runs.keys())

    workflow_runs = runs.get("workflow_runs")
    if not workflow_runs:
        print("No 'workflow_runs' key or it's empty. Full response:")
        print(runs)
        return

    for run in workflow_runs:
        run_id = run["id"]
        logs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}/logs"

        logs_resp = requests.get(logs_url, headers=headers)
        if logs_resp.status_code != 200:
            print(f"Error fetching logs for run {run_id}: {logs_resp.status_code}")
            print(logs_resp.text)
            continue

        with zipfile.ZipFile(BytesIO(logs_resp.content)) as z:
            out_dir = os.path.join(RAW_DIR, f"gha_run_{run_id}")
            os.makedirs(out_dir, exist_ok=True)
            z.extractall(out_dir)

        print(f"Saved logs for run: {run_id}")

if __name__ == "__main__":
    fetch_gha_logs()

