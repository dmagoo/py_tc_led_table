import os
import sys
import time
import random
from collections import deque

from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config
from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
import numpy as np

NODE_COUNT = 37
PIXELS_PER_RING = 8

"""
np.set_printoptions(threshold=np.inf)
def print_custom_array(array):
    print("[")
    for row in array:
        print("[", end=" ")
        for elem in row:
            print(elem, end=" ")
        print("]")  # End of row
    print("]")

"""

MAX_SNEK_LENGTH = 7

""" WIP
class TableBuffer():
    def __init__(self):
        self.fill()
        pass

    def fill(self, color=(0,0,0,0,0)):
        self.pixel_data = np.full((37, 8, 5), color)

    def blit(self, sprite):
        sprite_pixels = sprite.get_pixel_data()
        for (node_id, index), value in sprite_pixels.items():
            self.pixel_data[node_id, index] = value

class TableSprite():
    def __init__(self):
        pass

    def get_pixel_data(self):
        return {}

"""


MAX_SNEK_SPEED = 60
MIN_SNEK_SPEED = 0

class Snek():
    def __init__(self):
        self.color = (0, 30, 0, 0)
        self.length = 1
        # how many ticks to move a pixel
        # pixels per second
        self.speed = 7

        #node 0 pixel 0
        self.body = deque()
        self.body.appendleft((0,0))

        # node and pixel this snek seeks
        self.destination = (None, 0)

        # within the node, where the snake is headed
        self.current_node_target_pixel = None

        self.next_node = None
        self.next_node_entry_pixel = None

        self.last_tick_time = time.time()


    @property
    def head_position(self):
        if self.body:
            return self.body[0]
        else:
            return None

    @head_position.setter
    def head_position(self, new_value):
        current_node, current_pixel = self.head_position
        new_node, new_pixel = new_value

        if new_node != current_node or int(new_pixel) != int(current_pixel):
            self.body.appendleft(new_value)
            while len(self.body) > self.length:
                self.body.pop()
        else:
            self.body[0] = new_value

    def get_pixel_data(self):
        # add on unsupported alpha channel for now
        return {(node_id, int(partial_pixel)): self.color + (0,) for (node_id, partial_pixel) in self.body}

    def update_plan(self, table_api):
        dest_node_id, dest_pixel = self.destination
        head_node_id, head_pixel = self.head_position

        if dest_node_id is None:
            self.current_node_target_pixel = None
        elif head_node_id == dest_node_id:
            self.destination = (None, 0)
            self.current_node_target_pixel = None
            self.next_node = None
            self.next_node_entry_pixel = None
        else:
            path_nodes = table_api.getNodePath(head_node_id, dest_node_id)
            if len(path_nodes) > 1:
                self.next_node = path_nodes[1]
                self.current_node_target_pixel, self.next_node_entry_pixel = table_api.getFacingPixelIndexes(path_nodes[0], self.next_node)


    def tick(self, tick_count, table_api):
        current_time = time.time()
        delta_time =  current_time - self.last_tick_time

        self.update_plan(table_api)
        visited_nodes = [node_id for node_id, _ in self.body]

        head_node_id, head_pixel = self.head_position
        dest_node_id, _ = self.destination
        visited_nodes.append(head_node_id)

        next_pos = (head_pixel + (self.speed * delta_time)) % PIXELS_PER_RING

        if self.current_node_target_pixel == int(next_pos) and self.next_node_entry_pixel is not None:
            self.head_position = (self.next_node, self.next_node_entry_pixel)
            # force the snake to change from clockwise to counter-clock
            self.speed *= -1
            visited_nodes.append(self.next_node)
        #elif self.current_node_target_pixel is None or head_node_id == dest_node_id:
        else:
            self.head_position = (head_node_id, next_pos)
        self.last_tick_time = time.time()
        return visited_nodes



class SnekApp(TableController):
    def __init__(self, table_api, params={}):
        super().__init__(table_api)
        # WIP: self.table_buffer = TableBuffer()
        snek = Snek()
        snek.speed = 15

        snek2 = Snek()
        snek2.color = (0, 0, 30, 30)
        snek2.speed = 4

        snek3 = Snek()
        snek3.color = (0, 30, 30, 0)
        snek3.speed = 12

        snek4 = Snek()
        snek4.color = (0, 15, 30, 22)
        snek4.speed = 6

        self.snek_stack = [
            snek,
            snek2
            #snek3,
            #snek4
        ]

        self.current_snek_idx = -1
        self.prepareNextSnek()


    def prepareNextSnek(self):
        self.current_snek_idx = (self.current_snek_idx + 1) % len(self.snek_stack)

    def onNodeTouched(self, node_id):
        snek = self.snek_stack[self.current_snek_idx]
        snek.destination = (node_id, 0)
        snek.length = min(MAX_SNEK_LENGTH, snek.length + 1)
        self.prepareNextSnek()

    def draw_sneks(self):
        self.table_api.reset()
        for snek in self.snek_stack:
            for node_id, pixel in snek.body:
                self.table_api.setNodePixel(node_id, int(pixel), wrgb_tuple_to_int(snek.color))

    def doEffectLoop(self):

        visited_nodes = []
        for snek in self.snek_stack:
            visited_nodes.extend(snek.tick(self.tick_count, table_api=self.table_api))

        self.draw_sneks()

        for node_id in visited_nodes:
            self.updateLocalNode(node_id)

        self.table_api.refresh()
        #self.table_buffer.blit(self.snek)
        #print_custom_array(self.table_buffer.pixel_data)

def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)

    tc_led_table.init(config=led_table_config)
    app = SnekApp(tc_led_table)  # Create an instance of the App class

    # to run without the pygame display:
    app.use_display = False

    app.run()  # Start the app's main loop

if __name__ == "__main__":
    main()
