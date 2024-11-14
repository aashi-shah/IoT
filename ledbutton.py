#LED Circuit
#Connect the longer leg (anode) of the LED to GPIO pin 18 (physical pin 12).
#Connect the shorter leg (cathode) of the LED to a 220Ω resistor.
#Connect the other end of the resistor to the ground (GND).

#Button Circuit
#Connect one side of the button to GPIO pin 17 (physical pin 11).
#Connect the other side of the button to GND.

import RPi.GPIO as GPIO
import time

# Pin Definitions
LED_PIN = 18    # Pin to which LED is connected
BUTTON_PIN = 17 # Pin to which button is connected

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor

# Main program loop
try:
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            GPIO.output(LED_PIN, GPIO.HIGH)     # LED on
            time.sleep(0.5)                     # Delay of 0.5 seconds
            GPIO.output(LED_PIN, GPIO.LOW)      # LED off
            time.sleep(0.5)                     # Delay of 0.5 seconds
        else:
            GPIO.output(LED_PIN, GPIO.LOW)      # Keep LED off when button is not pressed
            time.sleep(0.1)                     # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Clean up all GPIO settings
