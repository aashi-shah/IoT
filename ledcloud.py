#Connect the longer leg (anode) of the LED to GPIO 18 (Physical Pin 12).
#Connect the shorter leg (cathode) to a 220Ω resistor.
#Connect the other end of the resistor to GND (Physical Pin 6) on the Raspberry Pi.

#sudo apt update
#sudo apt install python3-pip
#pip3 install requests

import RPi.GPIO as GPIO
import time
import requests

# ThingSpeak settings
CHANNEL_ID = 'YOUR_CHANNEL_ID'         # Replace with your ThingSpeak Channel ID
READ_API_KEY = 'YOUR_READ_API_KEY'     # Replace with your ThingSpeak Read API Key
WRITE_API_KEY = 'YOUR_WRITE_API_KEY'   # Replace with your ThingSpeak Write API Key
THINGSPEAK_READ_URL = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/1/last.json'
THINGSPEAK_WRITE_URL = 'https://api.thingspeak.com/update'

# GPIO setup
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def read_led_status():
    """Read LED control status from ThingSpeak"""
    try:
        response = requests.get(THINGSPEAK_READ_URL, params={'api_key': READ_API_KEY})
        if response.status_code == 200:
            data = response.json()
            led_status = data['field1']
            return led_status
        else:
            print(f"Failed to read from ThingSpeak: {response.status_code}")
    except Exception as e:
        print("An error occurred:", e)
    return None

def send_led_status(status):
    """Send LED status (ON/OFF) to ThingSpeak"""
    try:
        payload = {'api_key': WRITE_API_KEY, 'field1': status}
        response = requests.get(THINGSPEAK_WRITE_URL, params=payload)
        if response.status_code == 200:
            print("LED status sent to ThingSpeak successfully.")
        else:
            print("Failed to send data to ThingSpeak:", response.status_code)
    except Exception as e:
        print("An error occurred while sending data:", e)

try:
    # Main loop
    while True:
        # Step 1: Read LED control status from ThingSpeak
        led_status = read_led_status()
        
        if led_status == "ON":
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
            send_led_status("ON")            # Send LED status to ThingSpeak
            print("LED is ON")
        
        elif led_status == "OFF":
            GPIO.output(LED_PIN, GPIO.LOW)   # Turn off LED
            send_led_status("OFF")           # Send LED status to ThingSpeak
            print("LED is OFF")

        else:
            print("Received unknown command. Waiting...")

        # Polling interval to avoid excessive API requests (ThingSpeak allows 15s minimum)
        time.sleep(15)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    GPIO.cleanup()


HTTP link : https://api.thingspeak.com/update?api_key=YOUR_WRITE_API_KEY&field1=ON
