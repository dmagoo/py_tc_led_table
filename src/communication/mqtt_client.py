# src/communication/mqtt_client.py
import json
import paho.mqtt.client as mqtt

# MQTT Client Setup
def setup_mqtt_client(broker_address="127.0.0.1", client_id="default-client"):
    client = mqtt.Client(client_id=client_id)

    # Dictionary to store topic -> handler
    client._listeners = {}

    def _on_message(client, userdata, msg):
        # Dispatch to any registered listener for the topic
        if msg.topic in client._listeners:
            for callback in client._listeners[msg.topic]:
                callback(client, userdata, msg)

    client.on_message = _on_message

    # Attach helper methods
    def register_listener(self, topic, callback):
        if topic not in self._listeners:
            self._listeners[topic] = []
            self.subscribe(topic)
        self._listeners[topic].append(callback)

    client.register_listener = register_listener.__get__(client)
    client.connect(broker_address, 1883, 60)
    client.loop_start()
    return client

def publish_message(client, topic, message):
    result = client.publish(topic, message)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Message successfully published to {topic}. Message ID: {result.mid}")
    else:
        print(f"Failed to publish message to {topic}. Error code: {result.rc}")
    return result.rc

def publish_object(client, topic, data):
    return publish_message(client, topic, json.dumps(data))
