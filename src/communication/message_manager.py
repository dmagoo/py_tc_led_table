# src/communication/message_manager.py
# MessageManager is an app-level wrapper on top of the low-level MQTT client.
# It tracks the latest message received on each subscribed topic,
# along with a timestamp, and provides views or other systems with easy access
# to the most recent payload and its age in milliseconds.
# This avoids re-subscribing or re-parsing logic across the app.

import time

class MessageManager:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.latest_messages = {}  # topic -> (payload, timestamp)

    def register_topic(self, topic):
        def handler(msg):
            self.latest_messages[topic] = (msg.payload.decode(), time.time())
        self.mqtt_client.register_listener(topic, handler)
        self.mqtt_client.subscribe(topic)

    def get_latest(self, topic):
        if topic not in self.latest_messages:
            return None
        payload, timestamp = self.latest_messages[topic]
        age_ms = int((time.time() - timestamp) * 1000)
        return {"payload": payload, "age_ms": age_ms}
