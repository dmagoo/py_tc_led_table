"""
This example file shows how to control the leds on the TCTable
It uses python bindings to the table api to send artnet messages
To the clusters.  It also uses the api to act as a listener to
monitor sensor events
"""

import os
import sys
import random

from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config
from utils import rgb_tuple_to_int, fill_between
from TableController import TableController  # Import the App class from app.py

NODE_COUNT = 37

class ConnectNodes(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.test_node_a = -1
        self.test_node_b = -1
        color = tuple(params.get("color",  (100,200,100)))
        w,r,g,b = color
        self.color = (r,g,b)
    def doEffectLoop(self):
        self.test_node_a = -1
        self.test_node_b = -1
        if len(self.touched_node_ids) > 1:
            self.test_node_a,self.test_node_b = self.touched_node_ids[:2]

        path_nodes = self.table_api.getNodePath(self.test_node_a,  self.test_node_b)
        previous_node = None
        for current_node in range(37):
            self.table.nodes[current_node].touch_value = 100 if current_node in self.touched_node_ids else 0
            if current_node in path_nodes:
                path_index = path_nodes.index(current_node)
                if current_node == self.test_node_a or current_node == self.test_node_b:
                    self.table_api.fillNode(current_node, (rgb_tuple_to_int((200, 100,200))))
                    pass
                else:
                    (pixel_facing_start, pixelB) =  self.table_api.getFacingPixelIndexes(current_node,  self.test_node_a)
                    (pixel_facing_end, pixelB) =  self.table_api.getFacingPixelIndexes(current_node,  self.test_node_b)
                    fill = fill_between(8, pixel_facing_start, pixel_facing_end, self.color, direction = 'clockwise' if path_index % 2 == 0 else 'counter_clockwise')
                    self.table_api.fillNode(current_node, fill.astype(int).tolist(), 0)
                last_node = current_node
            else:
                self.table_api.fillNode(current_node, rgb_tuple_to_int((0,0,0)))

            self.updateLocalNode(current_node)

        self.table_api.refresh()


def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())

    tc_led_table.init(config=led_table_config)
    app = ConnectNodes(tc_led_table)  # Create an instance of the App class

    # to run without the pygame display:
    app.use_display = False

    app.run()  # Start the app's main loop

if __name__ == "__main__":
    main()
