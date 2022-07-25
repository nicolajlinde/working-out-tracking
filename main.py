import requests
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

API_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
ENDPOINT = os.getenv("ENDPOINT")


def exercise_calc(api_id, api_key):
    endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
    question = input("What exercise did you do?: ")

    headers = {
        "x-app-id": api_id,
        "x-app-key": api_key
    }

    exercise_params = {
        "query": question,
        "gender": "male",
        "weight_kg": 95,
        "height_cm": 182,
        "age": 32
    }

    response = requests.post(url=endpoint, json=exercise_params, headers=headers)
    data = response.json()
    return data


def insert_data_to_google_sheets(api_id, api_key, token, endpoint):
    data = exercise_calc(api_id, api_key)["exercises"]
    today = datetime.datetime.now()
    date = today.strftime("%Y/%m/%d")
    time = today.strftime("%H:%M:%S")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    for ex in data:
        params = {
            "workout": {
                "date": date,
                "time": time,
                "exercise": ex['name'].title(),
                "duration": f"{ex['duration_min']} min",
                "calories": f"{ex['nf_calories']} cal"
            }
        }

    response = requests.post(url=endpoint, json=params, headers=headers)
    response.raise_for_status()


insert_data_to_google_sheets(API_ID, API_KEY, TOKEN, ENDPOINT)
