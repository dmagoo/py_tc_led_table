# src/pygame/TableSimulator.py
from enum import Enum
import time
import pygame
from receiver import ArtNetReceiver
from utils import unpack_artnet_data_to_rgb_2d
from TableDisplay import TableDisplay
from communication.mqtt_client import publish_object

# Color constants
COLOR_INACTIVE = (30, 30, 30)
COLOR_TAPPED = (150, 150, 150)
COLOR_PINNED = (60, 120, 60)

class NodeState(Enum):
    INACTIVE = 1
    TAPPED = 2
    HOLDING = 3
    PINNED = 4

class TableSimulator(TableDisplay):
    def __init__(self, table_api, mqtt_client):
        super().__init__(table_api)
        self.mqtt_client = mqtt_client
        self.max_frame_rate = 100000

        self.artnet = ArtNetReceiver(ip="0.0.0.0", timeout=0.01)
        self.max_packets_per_tick = 100

        self.node_states = {}  # node_id: {state, timestamp, countdown}q
        self.max_tap_duration = 50  # fallback countdown if needed

        # Hold-time based countdown scaling (optional)
        self.hold_time_countdown_scale = 0.2 # Reasonable start: 0.2
        self.max_hold_time_countdown = 100    # Reasonable start: 100

    def tick(self):
        super().tick()
        self.getUpdates()
        self.handleInput()

    def handleNodeTouch(self, node_id, is_right_click=False):
        node = self.node_states.get(node_id, {"state": NodeState.INACTIVE})

        if is_right_click:
            if node["state"] == NodeState.PINNED:
                self.setNodeInactive(node_id)
            else:
                self.setNodePinned(node_id)
            return

        # Left click
        if node["state"] in (NodeState.INACTIVE, NodeState.TAPPED):
            self.startHolding(node_id)

    def handleNodeRelease(self, node_id):
        node = self.node_states.get(node_id)
        if not node or node["state"] != NodeState.HOLDING:
            return

        held_duration = time.time() - node["timestamp"]
        extra_countdown = min(
            int(held_duration * self.hold_time_countdown_scale),
            self.max_hold_time_countdown
        ) if self.hold_time_countdown_scale > 0 and self.max_hold_time_countdown > 0 else 0

        countdown = max(self.max_tap_duration, extra_countdown)
        self.node_states[node_id] = {"state": NodeState.TAPPED, "countdown": countdown}
        self.updateNodeColor(node_id)

    def startHolding(self, node_id):
        publish_object(self.mqtt_client, "ledtable/sensor/touch_event", {"nodeId": node_id, "touched": True})
        self.node_states[node_id] = {"state": NodeState.HOLDING, "timestamp": time.time()}
        self.updateNodeColor(node_id)

    def setNodePinned(self, node_id):
        publish_object(self.mqtt_client, "ledtable/sensor/touch_event", {"nodeId": node_id, "touched": True})
        self.node_states[node_id] = {"state": NodeState.PINNED}
        self.updateNodeColor(node_id)

    def setNodeInactive(self, node_id):
        publish_object(self.mqtt_client, "ledtable/sensor/touch_event", {"nodeId": node_id, "touched": False})
        self.node_states[node_id] = {"state": NodeState.INACTIVE}
        self.updateNodeColor(node_id)



    def updateNodeColor(self, node_id):
        node_info = self.node_states.get(node_id)
        if not node_info:
            return

        if node_info["state"] == NodeState.PINNED:
            self.table.nodes[node_id].color = COLOR_PINNED
        elif node_info["state"] == NodeState.TAPPED:
            brightness = node_info["countdown"] / self.max_tap_duration
            brightness = max(0.0, min(1.0, brightness))
            self.table.nodes[node_id].color = tuple(
                int(c * brightness + i * (1 - brightness))
                for c, i in zip(COLOR_TAPPED, COLOR_INACTIVE)
            )
        elif node_info["state"] == NodeState.HOLDING:
            held_duration = time.time() - node_info["timestamp"]
            extra_countdown = min(
                int(held_duration * self.hold_time_countdown_scale),
                self.max_hold_time_countdown
            ) if self.hold_time_countdown_scale > 0 and self.max_hold_time_countdown > 0 else 0
            brightness = extra_countdown / self.max_tap_duration
            brightness = max(0.0, min(1.0, brightness))
            self.table.nodes[node_id].color = tuple(
                int(c * brightness + i * (1 - brightness))
                for c, i in zip(COLOR_TAPPED, COLOR_INACTIVE)
            )

        else:
            self.table.nodes[node_id].color = COLOR_INACTIVE

    def handleNodeTicks(self):
        expired_nodes = []
        for node_id, node_info in self.node_states.items():
            if node_info["state"] == NodeState.TAPPED:
                node_info["countdown"] -= 1
                self.updateNodeColor(node_id)
                if node_info["countdown"] <= 0:
                    expired_nodes.append(node_id)
            if node_info["state"] == NodeState.HOLDING:
                self.updateNodeColor(node_id)

        for node_id in expired_nodes:
            self.setNodeInactive(node_id)

    def handleInput(self):
        self.handleNodeTicks()

        for event in self.event_list:
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicked_node_id = self.get_node_id_from_pos(event.pos)
                if clicked_node_id is not None:
                    self.handleNodeTouch(clicked_node_id, is_right_click=(event.button == 3))
            elif event.type == pygame.MOUSEBUTTONUP:
                clicked_node_id = self.get_node_id_from_pos(event.pos)
                if clicked_node_id is not None and event.button == 1:
                    self.handleNodeRelease(clicked_node_id)

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
