#Experiment 2 : 

#1. LED blink with time

#Connect the longer leg (anode) of the LED to GPIO pin 18 (physical pin 12).
#Connect the shorter leg (cathode) of the LED to a 220Ω resistor.
#Connect the other end of the resistor to the ground (GND).

import RPi.GPIO as GPIO
import time

# Pin Definitions
LED_PIN = 18  # Pin to which LED is connected

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Main program loop
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED on
        time.sleep(0.5)  # Delay of 0.5 seconds
        GPIO.output(LED_PIN, GPIO.LOW)   # LED off
        time.sleep(0.5)  # Delay of 0.5 seconds

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Clean up all GPIO settings
