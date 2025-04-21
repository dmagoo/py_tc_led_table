import math

from bootstrap import apply
apply()

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

from TableController import TableController  # Import the App class from app.py
from utils import wrgb_tuple_to_int
NODE_COUNT = 37
LEVELS =4

class StatusPulse(TableController):
    """ Dumb effect that fills every node in sequence, one pixel at a time """
    def __init__(self, table_api, params={}):
        super().__init__(table_api)
        self.changed = True

        self.base_color = tuple(params.get("color", [0, 250, 0, 20]))
        speed = params.get("speed", 1.0)
        self.frequency = 0.01 * speed  # higher speed = faster pulse

        self.phase_offset = math.pi / 2


    def doEffectLoop(self):
        #brightness = (math.sin(self.tick_count * self.frequency - self.phase_offset) + 1) / 2
        brightness = (math.sin(self.tick_count * self.frequency - self.phase_offset) + 1) / 2
        #brightness = brightness ** 2  # slows rise, quickens fall
        #apparent_color = wrgb_tuple_to_int(tuple([int(v * brightness ) for v in self.base_color]))
        #[self.table_api.fillNode(node_id, wrgb_tuple_to_int(apparent_color)) for node_id in range(NODE_COUNT)]


        for level in range(LEVELS):
            #offset = math.sin((level / LEVELS) * math.pi)  # or **2 for ease-in/out
            #offset = level / LEVELS  # linear but unique

            #offset = math.sin((level / (LEVELS - 1)) * math.pi / 2)  # monotonic

            offset = ((LEVELS-level)/LEVELS)*.39

            #apparent_brightness = (brightness + offset) % 1

            phase = (self.tick_count * self.frequency + offset) * 2 * math.pi
            apparent_brightness = (math.sin(phase - math.pi / 2) + 1) / 2
            apparent_brightness = apparent_brightness ** 2

            

            #apparent_brightness = (brightness + level / LEVELS) % 1
            #apparent_color = wrgb_tuple_to_int(tuple([int(v * brightness ) for v in self.base_color]))
            apparent_color = wrgb_tuple_to_int(tuple([int(v * apparent_brightness ) for v in self.base_color]))
            for neighbor_node_id in self.table_api.getNodeNeighbors(0, level):
                self.table_api.fillNode(neighbor_node_id, apparent_color)
        
        self.changed = True
        if self.changed:
            self.table_api.refresh()
            self.changed = False

    
def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)
    tc_led_table.init(config=led_table_config)
    app = StatusPulse(tc_led_table)
    app.use_display  = False
    app.run()
if __name__ == "__main__":
    main()
