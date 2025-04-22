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

from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config
from utils import wrgb_tuple_to_int
from TableController import TableController

NODE_COUNT = 37

def get_random_color():
    return (
        random.randint(0, 33),
        random.randint(11, 255),
        random.randint(30, 180),
        random.randint(0, 120)
    )

class TestNode(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.color = tuple(params.get("color", get_random_color()))
        self.node_states = {}
        
    def onNodeTouched(self, node_id):
        if self.node_states.get(node_id) is None:
            self.node_states[node_id] = self.color #get_random_color()
        else:
            self.node_states[node_id] = None

    def doEffectLoop(self):
        for node_id in range(NODE_COUNT):
            color = self.node_states.get(node_id)
            if not color:
                color = (0,0,0,0)
            self.table_api.fillNode(node_id, wrgb_tuple_to_int(color))
        self.table_api.refresh()


def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)
    tc_led_table.init(config=led_table_config)
    app = TestNode(tc_led_table)
    app.use_display  = False
    app.run()
if __name__ == "__main__":
    main()
