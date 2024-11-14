#sudo apt update
#sudo apt install mosquitto mosquitto-clients

#Connect the anode (long leg) of the LED to GPIO 17 (Physical Pin 11).
#Connect the cathode (short leg) to one end of a 220Ω resistor, and connect the other end of the resistor to GND (Physical Pin 6).

#sudo systemctl enable mosquitto
#sudo systemctl start mosquitto

#sudo apt install python3-pip
#pip3 install paho-mqtt RPi.GPIO


import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

# MQTT settings
BROKER_ADDRESS = "localhost"  # Use "localhost" if the broker is running on the same Raspberry Pi
LED_TOPIC = "home/led"

# GPIO setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe(LED_TOPIC)  # Subscribe to LED control topic

def on_message(client, userdata, msg):
    command = msg.payload.decode().lower()  # Decode message payload
    if command == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
    elif command == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")

# MQTT client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_ADDRESS, 1883, 60)  # Connect to the broker

try:
    client.loop_forever()  # Keep the client running to listen for messages
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    GPIO.cleanup()
