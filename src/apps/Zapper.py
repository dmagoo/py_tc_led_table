from enum import Enum

from utils import wrgb_tuple_to_int
from effects.chain_effect import ChainEffect
from effects.pixel_color_effect import PixelColorEffect
from generators.sine_generator import SineGenerator
from generators.tween_generator import TweenGenerator
from generators.composite_generator import CompositeGenerator
from apps.AppBase import AppBase

class State(Enum):
    WAITING = 1
    THINKING = 2
    FIRING = 3

class Zapper(AppBase):
    def __init__(self, table_api, params={}):
        super().__init__(table_api, params)
        self.reset()

    def reset(self):
        self.difficulty = 1

        self.base_nodes = {
            25: {
                "node_id": 25,
                "state": State.WAITING,
                "state_counter": 0,
                "effects": []
            },
            9: {
                "node_id": 9,
                "state": State.WAITING,
                "state_counter": 0,
                "effects": []
            }
        }
        all_effects = []

    def handle_node_touched(self, node_id):
        if node_id not in self.base_nodes.keys():
            return
        base_node = self.base_nodes.get(node_id)
        if base_node["state"] == State.WAITING:
            print("we were waiting, now we are thinking")
            base_node["state"] = State.THINKING
            base_node["state_countr"] = 0

    def handle_node_untouched(self, node_id):
        if node_id not in self.base_nodes.keys():
            return
        base_node = self.base_nodes.get(node_id)
        if base_node["state"] == State.THINKING:
            print("we were thinking, now we are firing")
            base_node["state"] = State.FIRING
            base_node["state_counter"] = 0

    def begin_node_state(self, base_node):
        base_node["effects"] = []
        base_node["state_data"] = {}
        
        # waiting to be clicked
        if base_node["state"] == State.WAITING:
            sine_gen = SineGenerator(frequency=0.5)
            # okay duration is odd, tweens are not meant to tween this way
            tween_gen = TweenGenerator(range=((0, 0, 0, 0), (0, 10, 50, 30)), duration=1.001)
            throb_gen = CompositeGenerator(sine_gen, tween_gen)
            pixel_targets = [(base_node["node_id"], i) for i in range(8)]
            throb_effect = PixelColorEffect(
                self.table_api,
                {},
                throb_gen,
                pixel_targets
            )
            base_node["effects"].append(throb_effect)
        
    def update_node_states(self):
        for base_node in self.base_nodes.values():
            if base_node["state_counter"] == 0:
                self.begin_node_state(base_node)
            base_node["state_counter"] += 1

            # todo: look at state of node and change state as needed
            
    def advance_effects(self, tick, delta_time):
        for base_node in self.base_nodes.values():
            [effect.tick(delta_time, tick) for effect in base_node["effects"]]

    def apply_effects(self):
        for base_node in self.base_nodes.values():
            for effect in base_node["effects"]:
                 effect_updates = effect.get_pixel_updates()
                 # perhaps add this to some api wrapper?
                 # apply_pixel_effects or something?
                 for nid, pixels in effect_updates.items():
                     for idx, color in enumerate(pixels):
                         if color is not None:
                             self.table_api.setNodePixel(nid, idx, wrgb_tuple_to_int(color))
            

    def loop(self, tick, delta_time):
        self.update_node_states()
        self.advance_effects(tick, delta_time)
        self.apply_effects()
        self.table_api.refresh()
