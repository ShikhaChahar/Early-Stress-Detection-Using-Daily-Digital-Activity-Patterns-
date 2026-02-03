

import datetime
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Scopes needed for Google Fit
SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.sleep.read"
]

TOKEN_FILE = "token.pkl"
CLIENT_SECRET_FILE = "client_secret.json"


def authenticate():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return creds


def fetch_google_fit_data():
    creds = authenticate()
    headers = {"Authorization": f"Bearer {creds.token}"}

    end_time = int(datetime.datetime.utcnow().timestamp() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)  # last 24 hours

    dataset_id = f"{start_time}-{end_time}"

    # Step Count
    steps_url = (
        "https://www.googleapis.com/fitness/v1/users/me/"
        f"dataSources/derived:com.google.step_count.delta:com.google.android.gms:estimated_steps/"
        f"datasets/{dataset_id}"
    )

    steps_resp = requests.get(steps_url, headers=headers).json()

    steps = 0
    for point in steps_resp.get("point", []):
        steps += point["value"][0]["intVal"]

    # Sleep (summary)
    sleep_url = (
        "https://www.googleapis.com/fitness/v1/users/me/"
        f"sessions?startTimeMillis={start_time}&endTimeMillis={end_time}"
    )

    sleep_resp = requests.get(sleep_url, headers=headers).json()

    sleep_minutes = 0
    for session in sleep_resp.get("session", []):
        if session.get("activityType") == 72:  # Sleep
            start = int(session["startTimeMillis"])
            end = int(session["endTimeMillis"])
            sleep_minutes += (end - start) / (1000 * 60)

    return {
        "steps": steps,
        "sleep_hours": round(sleep_minutes / 60, 2)
    }


if __name__ == "__main__":
    data = fetch_google_fit_data()
    print("Google Fit Data:", data)
