"""
This class can control the leds on the TCTable
It uses python bindings to the table api to send artnet messages
To the clusters.  It also uses the api to act as a listener to
monitor sensor events
"""
import os
import sys
import time
import random
import json
script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append(os.path.abspath('cpplib/python_bindings/Release'))

import tc_led_table
from utils import int_to_wrgb_tuple
from settings import get_config_value
from communication.mqtt_client import setup_mqtt_client

NODE_COUNT = 37

from TableDisplay import TableDisplay  # Import the App class from app.py

class TableController(TableDisplay):
    def __init__(self, table_api):
        super().__init__(table_api)

        self.screen_background_color = (0, 0, 0)
        self.broadcast = True
        self.max_frame_rate = 60
        # keep a list of touched nodes
        # but newer-touches are at the 
        # beginning
        self.touched_node_ids = []

        self.last_effect_loop = time.time()
        
        # Set up MQTT client for touch events
        self.mqtt_client = self._setup_mqtt_client()

    def _setup_mqtt_client(self):
        """Internal method to set up MQTT client for touch events"""
        try:
            broker = get_config_value("TableController", "mqtt_broker_address", "MQTT_BROKER_ADDRESS", default="localhost")
            client_id = get_config_value("TableController", "mqtt_client_id", "MQTT_CLIENT_ID", default=f"table-controller-{random.randint(1000,9999)}")
            mqtt_client = setup_mqtt_client(broker_address=broker, client_id=client_id)
            
            # Register for touch events
            mqtt_client.register_listener("ledtable/sensor/touch_event", self._handle_mqtt_touch)
            print(f"[DEBUG] TableController: MQTT client connected to {broker} as {client_id}")
            return mqtt_client
        except Exception as e:
            print(f"[WARNING] TableController: Could not connect to MQTT broker: {e}")
            return None

    def _handle_mqtt_touch(self, client, userdata, msg):
        """Internal MQTT touch event handler"""
        try:
            payload = json.loads(msg.payload.decode())
            node_id = payload["nodeId"]
            touched = payload["touched"]
            print(f"[DEBUG] TableController: Received MQTT touch event - node {node_id}, touched={touched}")
            
            # Forward to the standard touch handler
            self.handle_touch_event(node_id, touched)
        except Exception as e:
            print(f"[ERROR] TableController: Error handling MQTT touch: {e}")

    def tick(self):
        super().tick()
        self.doEffectLoop()
        self.last_effect_loop = time.time()

    def quit(self):
        super().quit()
        print("quitting effect")
        self.table_api.reset()
        self.table_api.refresh()


    def doEffectLoop(self):
        pass

    def onNodeTouched(self, node_id):
        pass

    def onNodeUntouched(self, node_id):
        pass

    def updateLocalNode(self, node_id):
        buffer = self.table_api.getNodePixelBuffer(node_id)
        self.table.nodes[node_id].colors = [int_to_wrgb_tuple(wrgb_int) for wrgb_int in buffer]


    def handle_touch_event(self, node_id, touched):
        print(f"[DEBUG] TableController: handle_touch_event called - node {node_id}, touched={touched}")
        if touched:
            if node_id not in self.touched_node_ids:
                self.touched_node_ids.insert(0, node_id)
                print(f"[DEBUG] TableController: Calling onNodeTouched({node_id})")
                self.onNodeTouched(node_id)
        else:
            if node_id in self.touched_node_ids:
                self.touched_node_ids.remove(node_id)
                print(f"[DEBUG] TableController: Calling onNodeUntouched({node_id})")
                self.onNodeUntouched(node_id)


