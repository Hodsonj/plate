import requests
import os 

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


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




# Loop to check plates 1 to 100
#for i in range(0, 101):
 #   plate_number = str(i)  # Format the plate number as 001, 002, ..., 100
 #   check_plate_availability(plate_number)
check_plate_availability("nak1ug1y")

