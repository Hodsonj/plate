import requests


# Define the base URL for the availability check
base_url = "https://bmvonline.dps.ohio.gov/bmvonline/oplates/PlatePreview"

# Define the parameters for the request (you can adjust these values)
for i in range(1,101):
    params = {
        "plateNumber": str(i),  # The license plate you want to check (e.g., "RROJON")
        "vehicleClass": "PC",      # Adjust vehicle class if necessary (PC is Personal Car)
        "organizationCode": "0",   # Organization code, as per the form data
    }

    # Define headers (these are similar to what the browser sends)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    # Send the GET request to check availability
    response = requests.get(base_url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Optionally, you can print the full response content to check the page
        # print(response.text)
        
        # Check the availability status based on the response
        if "available" in response.text:
            print(f"The plate {i} is available!")
        else:
            print(f"The plate {i} is not available.")
    else:
        print(f"Request failed with status code: {response.status_code}")
