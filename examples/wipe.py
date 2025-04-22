from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
from node_geometry import get_row_grouped_node_ids, convert_flat_to_pointy
NODE_COUNT = 37

import time

class Wipe(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.changed = True
        self.color = wrgb_tuple_to_int(tuple(params.get("color", (50,50,50,50))))
        speed = params.get("speed", 20)
        if speed == 0:
            self.interval_ms = 200
        else:
            self.interval_ms = 100 / speed


        flat = get_row_grouped_node_ids(table_api, ring_count=4, scan_axis='r')
        # not fully working yet
        #pointy = convert_flat_to_pointy(flat)
        self.wipe_rows = flat

        self.current_row = 0
        self.last_update = time.time() * 1000  # current time in ms

    def doEffectLoop(self):
        now = time.time() * 1000  # current time in ms
        if self.current_row < len(self.wipe_rows):
            if now - self.last_update >= self.interval_ms:
                for nodeId in self.wipe_rows[self.current_row]:
                    self.table_api.fillNode(nodeId, self.color)
                self.current_row += 1
                self.last_update = now
                self.changed = True

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
    app = Wipe(tc_led_table)
    app.use_display  = False
    app.run()
if __name__ == "__main__":
    main()
