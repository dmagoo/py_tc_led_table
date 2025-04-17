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

        self.node_wrgb = [0,0,0,0]
        self.changed = False

        self.max_frame_rate = 60

    def onNodeTouched(self, node_id):
        if node_id == 0:
            self.node_wrgb = [0,0,0,0]
        if node_id == 1:
             self.node_wrgb[0] = min(self.node_wrgb[0] + 5, 255)
        if node_id == 2:
             self.node_wrgb[1] = min(self.node_wrgb[1] + 5, 255)
        if node_id == 3:
             self.node_wrgb[2] = min(self.node_wrgb[2] + 5, 255)
        if node_id == 4:
             self.node_wrgb[3] = min(self.node_wrgb[3] + 5, 255)

        if node_id == 17:
             self.node_wrgb[3] = min(self.node_wrgb[3] + 5, 255)
             
        self.changed = True
    def doEffectLoop(self):
        if self.changed:
            print("new color:")
            print(self.node_wrgb)
            print(wrgb_tuple_to_int(self.node_wrgb))
            print(hex(wrgb_tuple_to_int(self.node_wrgb)))
            self.table_api.fillNode(0, wrgb_tuple_to_int(self.node_wrgb))
            self.updateLocalNode(0)
            self.table_api.refresh()
            self.changed = False


def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)

    tc_led_table.init(config=led_table_config)
    app = ControllerApp(tc_led_table)  # Create an instance of the App class
    app.run()  # Start the app's main loop

if __name__ == "__main__":
    main()
