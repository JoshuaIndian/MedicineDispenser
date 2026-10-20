import random
import time
from datetime import datetime, timezone

import httpx

API_URL = "http://127.0.0.1:8000"
DISPENSER_ID = 601


def generate_sensor_reading():
    return {
        "dispenser_id": DISPENSER_ID,
        "recorded_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "weight_grams": round(
            random.uniform(70, 90), 2
        ),
        "temperature_c": round(
            random.uniform(25, 30), 2
        ),
        "humidity_pct": round(
            random.uniform(60, 75), 2
        ),
        "rfid_detected": random.choice([True, False]),
        "fingerprint_verified": random.choice([True, False]),
    }


def main():
    print("Smart Medicine Dispenser simulator started.")
    print(f"API: {API_URL}")

    while True:
        reading = generate_sensor_reading()

        try:
            response = httpx.post(
                f"{API_URL}/sensors/readings",
                json=reading,
                timeout=10,
            )

            print("Sent:", reading)
            print("HTTP status:", response.status_code)
            print("Response:", response.text)

        except httpx.HTTPError as exc:
            print("Request failed:", exc)

        time.sleep(10)


if __name__ == "__main__":
    main()