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
        random.randint(11, 255),
        random.randint(30, 180),
        random.randint(0, 120)
    )

class Ripple(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.default_ripple_time = params.get("speed", 20)
        self.color = tuple(params.get("color", get_random_color()))

        self.neighbor_ripple_time = int(self.default_ripple_time * 1.4)
        self.ripples_per_event = 1.3

        self.ripple_timers = {}
        self.ripple_brightness = {}

        
    def onNodeTouched(self, node_id):
        """
        Starts a ripple effect from the touched node and propagates it to nearby nodes.
        - The touched node gets full brightness and default duration.
        - Neighbor nodes at levels 1–4 are triggered with increasing delay and decreasing brightness.
        - If a neighbor is already active, its brightness is boosted (but not lowered).
        - Timing and brightness scaling per level are defined in a config list for easy future customization.
        """
        self.ripple_timers[node_id] = self.default_ripple_time
        self.ripple_brightness[node_id] = 1

        neighbor_ripple_settings = [
            (1, 1.0, 0.2),
            (2, 1.3, 0.08),
            (3, 1.7, 0.01),
            (4, 2.0, 0.005),
        ]

        # self.color = get_random_color()
        
        for level, time_factor, min_brightness in neighbor_ripple_settings:
            for neighbor_node_id in self.table_api.getNodeNeighbors(node_id, level):
                if neighbor_node_id >= 0:
                    self.ripple_timers[neighbor_node_id] = self.neighbor_ripple_time * time_factor
                    old_brightness = self.ripple_brightness.get(neighbor_node_id, 0)
                    self.ripple_brightness[neighbor_node_id] = max(min_brightness, old_brightness)


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
                # base color of the ripple
                base_r, base_g, base_b = self.color
                #base_r, base_g, base_b = (244, 40, 0)

                # range of the color as it ripples
                # allowing a more complex fade
                amp_r, amp_g, amp_b = (0.78, 0.43, 1.0)
                # Random amplitude per channel (variation range: ±10% to ±100%)
                #amp_r = round(random.uniform(0.1, 1.0), 2)
                #amp_g = round(random.uniform(0.1, 1.0), 2)
                #amp_b = round(random.uniform(0.1, 1.0), 2)

                v1low = base_r * (1 - amp_r)
                v1high = base_r * (1 + amp_r)
                v1range_width = v1high - v1low

                v2low = base_g * (1 - amp_g)
                v2high = base_g * (1 + amp_g)
                v2range_width = v2high - v2low

                v3low = base_b * (1 - amp_b)
                v3high = base_b * (1 + amp_b)
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
    app = Ripple(tc_led_table)
    app.use_display  = False
    app.run()
if __name__ == "__main__":
    main()
