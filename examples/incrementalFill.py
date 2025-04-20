from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
NODE_COUNT = 37
PIXELS_PER_NODE = 8
import time

class IncrementalFill(TableController):
    """ Dumb effect that fills every node in sequence, one pixel at a time """
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.changed = True
        self.color = wrgb_tuple_to_int((50, 50, 50, 50))
        #self.interval_ms = 50  # time between row fills
        self.interval_ms = 0
        self.current_node = 0
        self.current_pixel = 0

        self.last_update = time.time() * 1000  # current time in ms

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
