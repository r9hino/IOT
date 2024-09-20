import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import paho.mqtt.client as mqtt
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# MQTT setup
BROKER = "localhost"
PORT = 51883
SUBSCRIBE_TOPIC = "sensor/request"
PUBLISH_TOPIC = "sensor/i2c"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Initialize I2C and ADS1115
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)
    channel = AnalogIn(ads, ADS.P0)
except Exception as e:
    logging.error(f"Failed to initialize I2C or ADS1115: {e}")
    raise SystemExit

# Read sensor data
def read_sensor():
    try:
        return {
            "analog_value": channel.value,
            "voltage": channel.voltage
        }
    except Exception as e:
        logging.error(f"Error reading from sensor: {e}")
        return None

# Connect to the MQTT broker
def connect_mqtt():
    try:
        client.connect(BROKER, PORT, 60)
    except Exception as e:
        logging.error(f"Failed to connect to MQTT broker: {e}. Will auto-reconnect.")
        #time.sleep(5)
        #connect_mqtt()  # Retry connection

# Callback for when a message is received on the subscribed topic
def on_message(client, userdata, msg):
    logging.info(f"Received message: {msg.payload.decode()}")
    
    # Read sensor data
    sensor_data = read_sensor()
    if sensor_data:
        client.publish(PUBLISH_TOPIC, json.dumps(sensor_data))
        logging.info(f"Published sensor data: {sensor_data}")
    else:
        logging.error("No sensor data available to publish.")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        logging.info(f"Connected to MQTT broker at {BROKER}:{PORT}")
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
        client.subscribe(SUBSCRIBE_TOPIC)
    else:
        logging.error(f"Connection failed with code {rc}")

# Callback for connection issues
def on_disconnect(client, userdata, rc, properties=None, reasonCode=None):
    logging.warning("Unexpected MQTT disconnection. Will auto-reconnect")

# Main loop
def main():
    connect_mqtt()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect  # Set the disconnect callback
    client.loop_start()

    try:
        while True:
            time.sleep(5)  # Keep the script running
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
    finally:
        logging.info("Script interrupted. Exiting.")

if __name__ == "__main__":
    main()
