"""
This example file shows how to control the leds on the TCTable
It uses python bindings to the table api to send artnet messages
To the clusters.  It also uses the api to act as a listener to
monitor sensor events
"""
import os
import sys
import time
import random
import math

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import platform

bindings_dir = 'lib/tc_led_table/python_bindings'
if platform.system() == 'Windows':
    bindings_dir = os.path.join(bindings_dir, 'Release')

sys.path.append(os.path.abspath(bindings_dir))



import tc_led_table
from settings import add_controller_config, add_sensor_listener_config
from utils import wrgb_tuple_to_int
from TableController import TableController  # Import the App class from app.py

NODE_COUNT = 37

class ControllerApp(TableController):
    def __init__(self, table_api):
        super().__init__(table_api)
        self.default_ripple_time = 29
        self.neighbor_ripple_time = int(self.default_ripple_time * 1.4)
        self.ripples_per_event = 1.3

        self.ripple_timers = {}
        self.ripple_brightness = {}

        self.max_frame_rate = 60

    def onNodeTouched(self, node_id):
        self.ripple_timers[node_id] = self.default_ripple_time
        l1_neighbor_nodes = self.table_api.getNodeNeighbors(node_id, 1)
        l2_neighbor_nodes = self.table_api.getNodeNeighbors(node_id, 2)
        l3_neighbor_nodes = self.table_api.getNodeNeighbors(node_id, 3)
        self.ripple_brightness[node_id] = 1

        for neighbor_node_id in l1_neighbor_nodes:
            if neighbor_node_id >= 0:
                if self.ripple_timers.get(neighbor_node_id):
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time
                    self.ripple_brightness[neighbor_node_id] = max(0.8, self.ripple_brightness[neighbor_node_id])
                else:
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time
                    self.ripple_brightness[neighbor_node_id] = 0.8

        for neighbor_node_id in l2_neighbor_nodes:
            if neighbor_node_id >= 0:
                if self.ripple_timers.get(neighbor_node_id):
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time * 1.3
                    self.ripple_brightness[neighbor_node_id] = max(0.7, self.ripple_brightness[neighbor_node_id])
                else:
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time * 1.3
                    self.ripple_brightness[neighbor_node_id] = 0.6

        for neighbor_node_id in l3_neighbor_nodes:
            if neighbor_node_id >= 0:
                if self.ripple_timers.get(neighbor_node_id):
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time * 1.7
                    self.ripple_brightness[neighbor_node_id] = max(0.3, self.ripple_brightness[neighbor_node_id])
                else:
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time * 1.7
                    self.ripple_brightness[neighbor_node_id] = 0.4


    def doEffectLoop(self):
        nodes_to_check = list(self.ripple_timers.keys())
        for node_id in nodes_to_check:
            self.ripple_timers[node_id] -= 1
            if self.ripple_timers[node_id] < 0:
                self.table_api.fillNode(node_id, 0x00000000)
                del self.ripple_timers[node_id]
                del self.ripple_brightness[node_id]
            # timer was given a high value so it could be delayed
            elif self.ripple_timers[node_id] > self.default_ripple_time:
                pass
            else:
                v1low = 10
                v1high = 80
                v1range_width = v1high - v1low

                v2low = 80
                v2high = 200
                v2range_width = v2high - v2low

                v3low = 0
                v3high = 120
                v3range_width = v3high - v3low

                t = self.ripple_timers[node_id]
                v1 = v1low + (v1range_width * (math.sin(math.pi * t / self.default_ripple_time * self.ripples_per_event) / 2 + 0.5))
                v2 = v2low + (v2range_width * (math.sin(math.pi * t / self.default_ripple_time * self.ripples_per_event) / 2 + 0.5))
                v3 = v3low + (v3range_width * (math.sin(math.pi * t / self.default_ripple_time * self.ripples_per_event) / 2 + 0.5))

                if self.ripple_brightness[node_id]:
                    b = self.ripple_brightness[node_id]
                    v1, v2, v3 = [v * b for v in (v1, v2, v3)]
                self.table_api.fillNode(node_id, wrgb_tuple_to_int((0, int(v1),int(v2),int(v3))))

            self.updateLocalNode(node_id)

        self.table_api.refresh()


def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)

    tc_led_table.init(config=led_table_config)
    app = ControllerApp(tc_led_table)  # Create an instance of the App class
    app.use_display  = False
    app.run()  # Start the app's main loop

if __name__ == "__main__":
    main()
