import os
import sys
import time
import random
from collections import deque

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config
from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
NODE_COUNT = 37
PIXELS_PER_RING = 8

MAX_SNEK_LENGTH = 7

class Snek():
    def __init__(self):
        self.color = (0, 255, 0, 0)
        self.length = 1
        # how many ticks to move a pixel
        # pixels per second
        self.speed = 7
        self.destination = (None, 0)

        #node 0 pixel 0
        self.body = deque()
        self.body.appendleft((0,0))

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

class ControllerApp(TableController):
    def __init__(self, table_api):
        super().__init__(table_api)
        self.snek = Snek()

        # within the node, where the snake is headed
        self.current_node_target_pixel = None

        # entry pixel for the next node
        self.next_node = None
        self.next_node_entry_pixel = None

    def onNodeTouched(self, node_id):
        self.snek.destination = (node_id, 0)
        self.snek.length = min(MAX_SNEK_LENGTH, self.snek.length + 1)

    def update_plan(self):
        #path_nodes = self.table_api.getNodePath(self.test_node_a,  self.test_node_b)
        #previous_node = None
        dest_node_id, dest_pixel = self.snek.destination
        head_node_id, head_pixel = self.snek.head_position

        if dest_node_id is None:
            self.current_node_target_pixel = None
        elif head_node_id == dest_node_id:
            self.snek.destination = (None, 0)
            self.current_node_target_pixel = None
            self.next_node = None
            self.next_node_entry_pixel = None
        else:
            path_nodes = self.table_api.getNodePath(head_node_id, dest_node_id)
            if len(path_nodes) > 1:
                self.next_node = path_nodes[1]
                self.current_node_target_pixel, self.next_node_entry_pixel = self.table_api.getFacingPixelIndexes(path_nodes[0], self.next_node)

    def move_snek(self):
        current_time = time.time()
        delta_time =  current_time - self.last_effect_loop

        head_node_id, head_pixel = self.snek.head_position
        dest_node_id, _ = self.snek.destination
        visited_nodes = [head_node_id]

        next_pos = (head_pixel + (self.snek.speed * delta_time)) % PIXELS_PER_RING

        if self.current_node_target_pixel == int(next_pos) and self.next_node_entry_pixel is not None:
            self.snek.head_position = (self.next_node, self.next_node_entry_pixel)
            self.snek.speed *= -1
            visited_nodes.append(self.next_node)
        #elif self.current_node_target_pixel is None or head_node_id == dest_node_id:
        else:
            self.snek.head_position = (head_node_id, next_pos)

        return visited_nodes

    def draw_snek(self):
        self.table_api.reset()
        for node_id, pixel in self.snek.body:
            self.table_api.setNodePixel(node_id, int(pixel), wrgb_tuple_to_int(self.snek.color))
        #head_node_id, head_pixel = self.snek.head_position
        #self.table_api.setNodePixel(head_node_id, int(head_pixel), wrgb_tuple_to_int(self.snek.color))

    def doEffectLoop(self):
        self.update_plan()
        visited_nodes = [node_id for node_id, _ in self.snek.body]
        visited_nodes.extend(self.move_snek())

        self.draw_snek()

        for node_id in visited_nodes:
            self.updateLocalNode(node_id)

        self.table_api.refresh()


def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)

    tc_led_table.init(config=led_table_config)
    app = ControllerApp(tc_led_table)  # Create an instance of the App class

    # to run without the pygame display:
    # self.use_display = False

    app.run()  # Start the app's main loop

if __name__ == "__main__":
    main()
