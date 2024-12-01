import network  # Import the network module to handle Wi-Fi connectivity
import time  # Import the time module for timing-related tasks (like delays)
import urequests  # Import the urequests module to make HTTP requests
from machine import Pin  # Import the Pin class from machine to handle GPIO pins (for the button)

# Wi-Fi credentials
SSID = "Your Wi-Fi network SSID (name)"  # 
PASSWORD = "Your Wi-Fi password"  # 

# Twilio credentials
TWILIO_SID = "Your Twilio Account SID"  # 
TWILIO_AUTH_TOKEN = "Your Twilio Auth Token"  # 
FROM_PHONE = "+The phone number you are sending messages from (Twilio-provided)"  # 
TO_PHONE = "+The phone number you want to send the message to"  # 

# Initialize push button
button = Pin(15, Pin.IN, Pin.PULL_UP)  # Set up a push button on GPIO pin 15 (with pull-up resistor)

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)  # Initialize the WLAN interface in station mode
    wlan.active(True)  # Activate the WLAN interface
    if not wlan.isconnected():  # If not already connected to Wi-Fi
        print("Connecting to Wi-Fi...")  # Print status message
        wlan.connect(SSID, PASSWORD)  # Attempt to connect to the Wi-Fi network with SSID and password
        while not wlan.isconnected():  # Wait until the connection is successful
            time.sleep(1)  # Sleep for 1 second to avoid busy-waiting
            print("Still trying...")  # Print a message to show connection is in progress
    print("Wi-Fi connected!")  # Print confirmation when connected
    print(f"IP Address: {wlan.ifconfig()[0]}")  # Print the assigned IP address

# Function to send SMS using Twilio
def send_sms(message):
    try:
        print("Sending SMS...")  # Print status message to indicate SMS sending attempt
        
        # Build the URL for the Twilio API, including the dynamic SID
        url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"  # Twilio API URL with SID dynamically inserted

        # Define the message data as a dictionary (corrected the 'data' variable)
        data = {
            'To': TO_PHONE,  # Recipient's phone number
            'From': FROM_PHONE,  # Your Twilio phone number (sender)
            'Body': message  # The content of the message you want to send
        }

        # Define the headers, including the Authorization header (correct format)
        headers = {
            'Authorization': f"Basic {TWILIO_SID}:{TWILIO_AUTH_TOKEN}",  # Basic authorization header with SID and Auth Token
            'Content-Type': 'application/x-www-form-urlencoded'  # Content type for the POST request
        }

        # Send the HTTP POST request to Twilio's API to send the SMS
        response = urequests.post(url, data=data, headers=headers)  # Send the request with the URL, data, and headers
        print(f"Response: {response.status_code} - {response.text}")  # Print the response status and text from Twilio
        
        # Check if the response status code is 201 (success)
        if response.status_code == 201:
            print("Message sent successfully!")  # Indicate success
        # Check if the response status code is 401 (authentication error)
        elif response.status_code == 401:
            print("Authentication failed! Check your SID, Auth Token, or phone numbers.")  # Print error message
        else:
            print(f"Failed to send message. Status code: {response.status_code}")  # Print error message for other status codes
        
        response.close()  # Close the response object to free resources

    except Exception as e:  # Catch any exceptions that occur during the process
        print(f"Error while sending SMS: {e}")  # Print the error message

# Connect to Wi-Fi
connect_to_wifi()  # Call the function to connect to the Wi-Fi network

# Monitor button presses
while True:
    if button.value() == 0:  # If the button is pressed (value is 0)
        print("Button Pressed!")  # Print message indicating button press
        send_sms("Button Pressed!")  # Send the SMS with the "Button Pressed!" message
        time.sleep(1)  # Sleep for 1 second to debounce the button (prevent multiple triggers)

