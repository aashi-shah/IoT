#VCC (or +): Connect to 3.3V on the Raspberry Pi (pin 1).
#Data: Connect to a GPIO pin, such as GPIO 4 (physical pin 7).
#GND: Connect to GND on the Raspberry Pi (pin 6).

#sudo apt update
#sudo apt install python3-pip
#pip3 install Adafruit_DHT

import Adafruit_DHT
import time

# Define sensor type and GPIO pin
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # GPIO pin where the data pin of DHT11 is connected

try:
    while True:
        # Read humidity and temperature
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

        # Check if reading was successful
        if humidity is not None and temperature is not None:
            print(f"Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")
        else:
            print("Failed to retrieve data from the sensor")

        time.sleep(2)  # Read every 2 seconds

except KeyboardInterrupt:
    print("Program stopped by User")


