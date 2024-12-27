import requests
import time
from flask import Flask
import threading


SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"


# Define the base URL for the availability check
base_url = "https://bmvonline.dps.ohio.gov/bmvonline/oplates/PlatePreview"

# Define headers (these are similar to what the browser sends)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

app = Flask(__name__)

def send_slack_notification(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code == 200:
        print("Slack message sent successfully!")
    else:
        print(f"Failed to send Slack message: {response.status_code}")

# Function to check license plate availability
def check_plate_availability(plate_number):
    # Define the parameters for the request
    params = {
        "plateNumber": plate_number,  # License plate number to check
        "vehicleClass": "PC",         # Vehicle class (Personal Car)
        "organizationCode": "0",      # Organization code
    }

    # Send the GET request to check availability
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Checking plate {plate_number}: Request successful!")
        # Check the availability status based on the response
        if "available" in response.text:
            print(f"Plate {plate_number} is available!")
            send_slack_notification(f"License plate: {plate_number} is available!")
        else:
            print(f"Not available {plate_number}.")
    else:
        print(f"Request for plate {plate_number} failed with status code: {response.status_code}")


# Function to check plates 1 to 100
def check_plates():
    # Loop to check plates 1 to 100
    for i in range(0, 101):
        plate_number = str(i)  # Format the plate number as 001, 002, ..., 100
        check_plate_availability(plate_number)
        time.sleep(10)  # Add a delay between requests to avoid overwhelming the server

# Route to trigger the plate checking process
@app.route("/check-plates")
def check_plates_route():
    # Start the plate checking in a separate thread so it doesn't block the server
    threading.Thread(target=check_plates).start()
    return "Plate availability check started!"


if __name__ == "__main__":
    # Run the Flask app on the port defined by Render
    app.run(host="0.0.0.0", port=5000)  # Use the port that Render assigns (5000 for local development, but Render will override it)
