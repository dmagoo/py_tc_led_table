from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int

NODE_COUNT = 37

def convert_flat_to_pointy(flat_rows):
    total_diagonals = sum(len(row) for row in flat_rows)
    num_rows = len(flat_rows)
    num_diagonals = num_rows * 2 - 1  # e.g., 7 → 13

    # Create empty target structure
    diagonals = [[] for _ in range(num_diagonals)]

    for row_index, row in enumerate(flat_rows):
        offset = row_index  # shift right with each lower row
        for i, val in enumerate(row):
            diagonals[i + offset].append(val)

    return diagonals


def get_row_grouped_node_ids(api, ring_count, scan_axis='r', reverse=False):
    if scan_axis not in ('q', 'r', 's'):
        raise ValueError("scan_axis must be 'q', 'r', or 's'")

    # Build all valid cube coordinates in a hex with center (0,0,0)
    coords = []
    for q in range(-ring_count + 1, ring_count):
        for r in range(-ring_count + 1, ring_count):
            s = -q - r
            if abs(s) < ring_count:
                coords.append((q, r, s))

    # Compute group key for each cube coordinate
    cube_with_ids = []
    for q, r, s in coords:
        if scan_axis == 'q':
            key = q
        elif scan_axis == 'r':
            key = r
        else:  # scan_axis == 's'
            key = s
        node_id = api.getNodeId(tc_led_table.CubeCoordinate(q, r, s))
        cube_with_ids.append((key, q, r, node_id))  # use q/r for left-right sorting

    # Sort: top-down (by key descending), then left to right (by q then r)
    cube_with_ids.sort(key=lambda t: (-t[0], t[1], t[2]))

    # Group by key
    rows = []
    current_key = None
    current_row = []
    for key, q, r, node_id in cube_with_ids:
        if key != current_key:
            if current_row:
                rows.append(current_row)
            current_row = [node_id]
            current_key = key
        else:
            current_row.append(node_id)
    if current_row:
        rows.append(current_row)

    if reverse:
        rows.reverse()

    return rows

import time

class Wipe(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.changed = True
        self.color = wrgb_tuple_to_int((50, 50, 50, 50))

        flat = get_row_grouped_node_ids(table_api, ring_count=4, scan_axis='r')
        # not fully working yet
        #pointy = convert_flat_to_pointy(flat)
        self.wipe_rows = flat

        self.current_row = 0
        self.interval_ms = 1000  # time between row fills
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


class OLDWipe(TableController):
    def __init__(self, table_api, params = {}):
        super().__init__(table_api)
        self.changed = True
        self.color = wrgb_tuple_to_int((50,50,50,50))
        #print(get_row_grouped_node_ids(table_api, 4, 'qr'))
        flat = get_row_grouped_node_ids(table_api, ring_count=4, scan_axis='r')
        pointy = convert_flat_to_pointy(flat)
        self.speed = 111 # todo, this
        self.wipe_rows = pointy
        self.current_row = 0


    def doEffectLoop(self):
        [self.table_api.fillNode(nodeId, self.color) for nodeId in self.wipe_rows[self.current_row]]

        # use a timer to 
        if(self.changed):
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
