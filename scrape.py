import requests
from bs4 import BeautifulSoup


# Step 1: Fetch the webpage
url = "https://bmvonline.dps.ohio.gov/bmvonline/oplates/specializedplates/1"  # Replace with the actual URL

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded"
}
response = requests.get(url, headers=headers)

# Step 2: Parse the HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Step 3: Locate the form
form = soup.find("form")
if not form:
    print("No form found on the page.")
    exit()

print("Form found!")

# Step 4: Extract input fields and construct the payload
payload = {}  # Initialize the payload dictionary
inputs = form.find_all("input")
for input_tag in inputs:
    name = input_tag.get("name")
    input_type = input_tag.get("type")
    value = input_tag.get("value", "")  # Default to empty if no value is set
    print(f"Name: {name}, Type: {input_type}, Value: {value}")
    if name:  # Only include named inputs in the payload
        payload[name] = value

# Step 5: Extract dropdowns (if any)
dropdowns = form.find_all("select")
for select_tag in dropdowns:
    name = select_tag.get("name")
    print(f"Dropdown Name: {name}")
    options = select_tag.find_all("option")
    for option in options:
        option_value = option.get("value")
        option_text = option.text.strip()
        print(f"  Option Value: {option_value}, Text: {option_text}")
        # Set a default value (e.g., the first option)
        if name and not payload.get(name):
            payload[name] = option_value

# Step 6: Define the payload and add the license plate number
payload['PersonalizedPlateNumber'] = "1"  # Replace with the plate number you want to check
print("___________")
print(payload)
# Step 7: Get the form's action URL
action_url = form.get("action")  # Relative action URL
full_url = requests.compat.urljoin(url, action_url)  # Build full URL if action is relative
print(full_url)
print("00000000000000")
# Step 8: Send a POST request to simulate form submission
response = requests.post(full_url, data=payload, headers=headers)

# Step 9: Check the response
if response.status_code == 200:
    print("Form submitted successfully!")
    
    # Step 10: Parse the response to check availability
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Look for a message or element that indicates availability
    availability_message = soup.find("div", {"class": "availability-status"})  # Adjust the selector as needed
    if availability_message:
        print("Availability Status:", availability_message.text.strip())
    else:
        print("Could not find availability status in the response.")
else:
    print(f"Failed to submit form. Status code: {response.status_code} Otherr: {response.text}")

