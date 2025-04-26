# src/pygame/TableSimulator.py
from enum import Enum
import time
import pygame
from receiver import ArtNetReceiver
from utils import unpack_artnet_data_to_rgb_2d
from TableDisplay import TableDisplay
from communication.mqtt_client import publish_object

class NodeClickBehavior(Enum):
    TOUCH_SENSOR_BRIEF = 1
    TOUCH_SENSOR_MOMENTARY = 2
    TOUCH_SENSOR_TOGGLE = 4

class TableSimulator(TableDisplay):
    def __init__(self, table_api, mqtt_client):
        super().__init__(table_api)
        self.mqtt_client = mqtt_client
        # receiver has to be high, or there is a big back log
        self.max_frame_rate = 100000
        self.last_effect_loop = time.time()

        self.artnet = ArtNetReceiver(ip="0.0.0.0", timeout=0.01)
        self.max_packets_per_tick = 100

        self.node_click_behavior = NodeClickBehavior.TOUCH_SENSOR_BRIEF
        # number of ticks for newly clicked node to decay
        self.node_click_duration = 50
        self.node_timers = {}

    def tick(self):
        super().tick()
        self.getUpdates()
        self.handleInput()

    def handleNodeClick(self, node_id):
        old_val = self.table.nodes[node_id].touch_value
        new_value  = 0 if old_val > 50 else 100
        publish_object(self.mqtt_client, "ledtable/sensor/touch_event", {"nodeId": node_id, "touched": new_value > 50})
        # publish touch-event on
        self.table.nodes[node_id].touch_value = new_value

        if self.node_click_behavior == NodeClickBehavior.TOUCH_SENSOR_BRIEF:
            self.node_timers[node_id] = self.node_click_duration

    def handleNodeTicks(self):
        # Decay the nodes, and remove nodes that reach 0
        if self.node_click_behavior == NodeClickBehavior.TOUCH_SENSOR_BRIEF:
            nodes_to_remove = [node_id for node_id, value in self.node_timers.items() if value - 1 <= 0]
            self.node_timers = {node_id: value - 1 for node_id, value in self.node_timers.items() if value - 1 > 0}
            for node_id in nodes_to_remove:
                self.table.nodes[node_id].touch_value = 0
                publish_object(self.mqtt_client, "ledtable/sensor/touch_event", {"nodeId": node_id, "touched": False})

    def handleInput(self):
        self.handleNodeTicks()

        for event in self.event_list:
            if event.type == pygame.QUIT:
                # running = False
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_node_id = self.get_node_id_from_pos(event.pos)
                if clicked_node_id is not None:
                    self.handleNodeClick(clicked_node_id)
    
    def getUpdates(self):
        for _ in range(self.max_packets_per_tick):
            packet = self.artnet.receive()

            if packet is None:
                break

            universe = packet.universe
            data = packet.data
            colors = unpack_artnet_data_to_rgb_2d(data)

            if universe == 0:
                first_node = 0
            else:
                first_node = universe * 10 - 3

            for i in range(len(colors)):
                self.table.nodes[first_node + i].colors = colors[i]
