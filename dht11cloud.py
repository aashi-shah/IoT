#Go to ThingSpeak and create an account if you don’t have one.
#After logging in, click on Channels > My Channels > New Channel.
#Fill in the details:Add two fields: Temperature and Humidity (or as you prefer).
#Save the channel, and you’ll see a Channel ID and an API Key. Note the Write API Key.


#VCC (or +): Connect to 3.3V on the Raspberry Pi (Physical Pin 1).
#Data: Connect to GPIO 4 (Physical Pin 7) on the Raspberry Pi.
#GND (or -): Connect to GND on the Raspberry Pi (Physical Pin 6).

import Adafruit_DHT
import time
import requests

# Sensor and GPIO setup
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin where the data pin of DHT11 is connected

# ThingSpeak Channel Settings
THINGSPEAK_URL = 'https://api.thingspeak.com/update'
WRITE_API_KEY = 'YOUR_WRITE_API_KEY'  # Replace with your ThingSpeak Write API Key

def send_to_thingspeak(temp, hum):
    try:
        # Prepare data to send to ThingSpeak
        payload = {
            'api_key': WRITE_API_KEY,
            'field1': temp,
            'field2': hum
        }
        # Send data to ThingSpeak
        response = requests.get(THINGSPEAK_URL, params=payload)

        # Check response status
        if response.status_code == 200:
            print("Data sent to ThingSpeak successfully.")
        else:
            print("Failed to send data to ThingSpeak:", response.status_code)
    except Exception as e:
        print("An error occurred while sending data:", e)

try:
    while True:
        # Read humidity and temperature
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        # Check if reading was successful
        if humidity is not None and temperature is not None:
            print(f"Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")
            # Send data to ThingSpeak
            send_to_thingspeak(temperature, humidity)
        else:
            print("Failed to retrieve data from the sensor")

        # ThingSpeak allows uploads every 15 seconds (or longer)
        time.sleep(15)

except KeyboardInterrupt:
    print("Program stopped by User")


