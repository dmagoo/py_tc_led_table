# src/communication/message_manager.py
# MessageManager is an app-level wrapper on top of the low-level MQTT client.
# It tracks the latest message received on each subscribed topic,
# along with a timestamp, and provides views or other systems with easy access
# to the most recent payload and its age in milliseconds.
# This avoids re-subscribing or re-parsing logic across the app.

import json
import time

class MessageManager:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.latest_messages = {}  # topic -> (payload, timestamp)

    def register_topic(self, topic):
        def handler(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode())
                self.latest_messages[topic] = (payload, time.time())
            except Exception as e:
                print(f"Error handling message on topic {topic}: {e}")

        self.mqtt_client.register_listener(topic, handler)

    def publish(self, topic, payload):
        try:
            message = json.dumps(payload)
            self.mqtt_client.publish(topic, message)
        except Exception as e:
            print(f"Error publishing to {topic}: {e}")

    def get_latest_message_from_topic(self, topic):
        if topic not in self.latest_messages:
            return None
        payload, timestamp = self.latest_messages[topic]
        age_ms = int((time.time() - timestamp) * 1000)
        return {"payload": payload, "age_ms": age_ms}

    def track_latest_message_from_topic(self, topic):
        if topic not in self.latest_messages:
            self.register_topic(topic)
