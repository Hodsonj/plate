import requests
from flask import Flask, jsonify
import time

app = Flask(__name__)

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Define the base URL for the availability check
base_url = "https://bmvonline.dps.ohio.gov/bmvonline/oplates/PlatePreview"

# Define headers (these are similar to what the browser sends)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}

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

@app.route('/check-plates', methods=['GET'])
def check_plates():
    # Loop to check plates 1 to 100
    for i in range(0, 101):
        plate_number = str(i)  # Format the plate number as 001, 002, ..., 100
        check_plate_availability(plate_number)

    return jsonify({"message": "Plate checking complete!"}), 200

def run_periodically():
    while True:
        # Call the check_plates function
        with app.app_context():
            check_plates()

        # Sleep for 14 minutes (840 seconds)
        time.sleep(840)

if __name__ == '__main__':
    # Start the periodic task in the background
    import threading
    threading.Thread(target=run_periodically, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
