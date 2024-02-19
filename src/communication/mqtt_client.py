import paho.mqtt.client as mqtt
import time

# MQTT Callback Functions
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("ledtable/clusters/0/touchSensor")
    publish_message(client, "ledtable/clusters/0/touchSensor", "Hello, LED Table!")

def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")
    # Add your message handling logic here

# MQTT Client Setup
def setup_mqtt_client(broker_address="broker.hivemq.com", topic="your/topic"):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, 1883, 60)
    client.subscribe(topic)

    return client

def publish_message(client, topic, message):
    result = client.publish(topic, message)

    # Check the result of the publish call
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Message successfully published to {topic}. Message ID: {result.mid}")
    else:
        print(f"Failed to publish message to {topic}. Error code: {result.rc}")

    # Optionally, return the result code for further use
    return result.rc

if __name__ == "__main__":
    client = setup_mqtt_client()
    client.loop_start()

    try:
        # Publish a test message
        # publish_message(client, "ledtable/clusters/0/touchSensor", "Hello, LED Table!")

        # Main loop to keep the script running
        while True:
            time.sleep(1)  # Add a delay to prevent overloading with messages
    except KeyboardInterrupt:
        print("Disconnecting from MQTT")
        client.disconnect()
