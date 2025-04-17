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
script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import tc_led_table
from utils import int_to_wrgb_tuple

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

    def tick(self):
        super().tick()
        self.updateTouchedNodeIds()
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

    def updateTouchedNodeIds(self):
        # Fetch the latest list of IDs
        all_touched = self.table_api.getAllTouchedNodeIds()

        # Create a set for efficient look-up
        all_touched_set = set(all_touched)
        old_touched_set = set(self.touched_node_ids)

        # Identify removed nodes and call onNodeUntouched for each
        removed_nodes = old_touched_set - all_touched_set
        for node_id in removed_nodes:
            self.onNodeUntouched(node_id)

        # Update touched_node_ids to only include currently touched nodes
        self.touched_node_ids = [id_ for id_ in self.touched_node_ids if id_ in all_touched_set]

        # Identify new nodes and call onNodeTouched for each, then add them to touched_node_ids
        new_items = [id_ for id_ in all_touched if id_ not in self.touched_node_ids]
        for node_id in new_items:
            self.onNodeTouched(node_id)

        # Prepend new items to maintain order with new items at the beginning
        self.touched_node_ids = new_items + self.touched_node_ids


