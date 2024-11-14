#Signal: Connect the signal wire (usually yellow/orange) to GPIO 17 (Physical Pin 11) on the Raspberry Pi.
#VCC: Connect the power wire (usually red) to 5V (Physical Pin 2).
#GND: Connect the ground wire (usually black or brown) to GND (Physical Pin 6) on the Raspberry Pi.

#sudo apt update
#sudo apt install python3-pip
#pip3 install RPi.GPIO requests


import RPi.GPIO as GPIO
import time
import requests

# ThingSpeak settings
CHANNEL_ID = 'YOUR_CHANNEL_ID'          # Replace with your ThingSpeak Channel ID
READ_API_KEY = 'YOUR_READ_API_KEY'      # Replace with your ThingSpeak Read API Key
THINGSPEAK_READ_URL = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/fields/1/last.json'

# Servo motor setup
SERVO_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set up PWM for servo control at 50Hz frequency
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)  # Initialize PWM with 0 duty cycle

def set_servo_angle(angle):
    """Sets the servo motor to a specified angle (0 to 180)"""
    # Calculate duty cycle for given angle
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

def get_servo_position():
    """Fetch the latest servo angle from ThingSpeak"""
    try:
        response = requests.get(THINGSPEAK_READ_URL, params={'api_key': READ_API_KEY})
        if response.status_code == 200:
            data = response.json()
            position = data['field1']
            return float(position)  # Convert to float for angle
        else:
            print(f"Failed to read from ThingSpeak: {response.status_code}")
    except Exception as e:
        print("An error occurred:", e)
    return None

try:
    # Main loop
    while True:
        # Fetch the target servo angle from ThingSpeak
        target_angle = get_servo_position()
        
        if target_angle is not None:
            print(f"Setting servo angle to: {target_angle}")
            set_servo_angle(target_angle)
        else:
            print("Failed to retrieve angle. Waiting for the next check.")

        # ThingSpeak allows a minimum 15-second update interval
        time.sleep(15)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    pwm.stop()
    GPIO.cleanup()


Explanation of the Code
THINGSPEAK_READ_URL: Specifies the URL to fetch the latest position data from ThingSpeak.
set_servo_angle(angle): Calculates the PWM duty cycle to rotate the servo to the specified angle.
Duty cycle calculation: For most servos, 0 degrees corresponds to about a 2% duty cycle, and 180 degrees to about 12%. The formula 2 + (angle / 18) is used to linearly scale the duty cycle based on the angle.
get_servo_position(): Retrieves the servo angle from ThingSpeak and parses it.
Main Loop: Checks ThingSpeak every 15 seconds for a new angle, then moves the servo to the specified position.

https://api.thingspeak.com/update?api_key=YOUR_WRITE_API_KEY&field1=90
