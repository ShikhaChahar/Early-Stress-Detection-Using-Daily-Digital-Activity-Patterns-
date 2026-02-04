import datetime
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

# -----------------------------
# Google Fit Scopes
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/fitness.activity.read",
    "https://www.googleapis.com/auth/fitness.sleep.read"
]

TOKEN_FILE = "token.pkl"
CLIENT_SECRET_FILE = "client_secret.json"


# -----------------------------
# Authentication
# -----------------------------
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


# -----------------------------
# Fetch aggregated step count
# -----------------------------
import datetime
import pytz

def fetch_steps_aggregated(headers):
    url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

    # Use LOCAL timezone (IST)
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)

    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

    start_time = int(start_of_day.timestamp() * 1000)
    end_time = int(now.timestamp() * 1000)

    body = {
        "aggregateBy": [{
            "dataTypeName": "com.google.step_count.delta"
        }],
        "bucketByTime": {
            "durationMillis": end_time - start_time
        },
        "startTimeMillis": start_time,
        "endTimeMillis": end_time
    }

    response = requests.post(url, headers=headers, json=body).json()

    steps = 0
    for bucket in response.get("bucket", []):
        for dataset in bucket.get("dataset", []):
            for point in dataset.get("point", []):
                steps += point["value"][0]["intVal"]

    return steps




# -----------------------------
# Fetch sleep duration (hours)
# -----------------------------
def fetch_sleep_hours(headers, start_time, end_time):
    url = (
        "https://www.googleapis.com/fitness/v1/users/me/"
        f"sessions?startTimeMillis={start_time}&endTimeMillis={end_time}"
    )

    response = requests.get(url, headers=headers).json()

    sleep_minutes = 0
    for session in response.get("session", []):
        if session.get("activityType") == 72:  # Sleep
            start = int(session["startTimeMillis"])
            end = int(session["endTimeMillis"])
            sleep_minutes += (end - start) / (1000 * 60)

    return round(sleep_minutes / 60, 2)


# -----------------------------
# Main Google Fit Fetcher
# -----------------------------
def fetch_google_fit_data():
    creds = authenticate()
    headers = {"Authorization": f"Bearer {creds.token}"}

    end_time = int(datetime.datetime.utcnow().timestamp() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)  # last 24 hours

    steps = fetch_steps_aggregated(headers)
    sleep_hours = fetch_sleep_hours(headers, start_time, end_time)

    print(f"✅ Step count fetched from Google Fit API: {steps}")

    return {
        "steps": steps,
        "sleep_hours": sleep_hours
    }


# -----------------------------
# Test Run
# -----------------------------
if __name__ == "__main__":
    data = fetch_google_fit_data()

    print("\n📊 Google Fit Data Summary")
    print("---------------------------")
    print(f"Steps       : {data['steps']}")
    print(f"Sleep Hours : {data['sleep_hours']}")
