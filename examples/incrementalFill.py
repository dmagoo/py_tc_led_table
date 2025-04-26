import random
from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config

from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
NODE_COUNT = 37
PIXELS_PER_NODE = 8
import time

def get_random_color():
    return (
        random.randint(11, 100),
        random.randint(30, 180),
        random.randint(0, 120),
        random.randint(0, 120)
    )

class IncrementalFill(TableController):
    """ Dumb effect that fills every node in sequence, one pixel at a time """
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.color = wrgb_tuple_to_int(tuple(params.get("color", get_random_color())))
        #self.interval_ms = 50  # time between row fills
        speed = params.get("speed", 20)
        if speed == 0:
            self.interval_ms = 200
        else:
            self.interval_ms = 100 / speed

        self.current_node = 0
        self.current_pixel = 0

        self.last_update = time.time() * 1000  # current time in ms
        self.changed = True

    def doEffectLoop(self):
        now = time.time() * 1000  # current time in ms

        if self.current_node < NODE_COUNT:
            if now - self.last_update >= self.interval_ms:
                self.table_api.setNodePixel(self.current_node, self.current_pixel, self.color)
                self.last_update = now
                self.changed = True

                self.current_pixel += 1
                if self.current_pixel >= PIXELS_PER_NODE:
                    self.current_pixel = 0
                    self.current_node += 1


        if self.changed:
            self.table_api.refresh()
            self.changed = False


"""
fillNode
setNodePixel
queueNodePixel
dequeueNodePixel
getNodeId
getNodePixelBuffer
getNodePath
getNodeNeighbors
getFacingPixelIndexes
getTouchState
getAllTouchedNodeIds
reset
refresh
"""
    
def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)
    tc_led_table.init(config=led_table_config)
    app = IncrementalFill(tc_led_table)
    app.use_display  = False
    app.run()
if __name__ == "__main__":
    main()
