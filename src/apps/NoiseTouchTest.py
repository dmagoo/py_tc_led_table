import time
from utils import wrgb_tuple_to_int
from effects.pixel_color_effect import PixelColorEffect
from generators.random_noise_generator import RandomNoiseGenerator
from apps.AppBase import AppBase

class NoiseTouchTest(AppBase):
    def __init__(self, table_api, params={}):
        super().__init__(table_api, params)
        self.active_effects = {}

        self.touch_min = params.get("touch_min", (0, 60, 0, 0))
        self.touch_max = params.get("touch_max", (0, 90, 0, 0))
        self.untouch_min = params.get("untouch_min", (0, 0, 0, 0))
        self.untouch_max = params.get("untouch_max", (0, 0, 1, 8))


        self.hold_time = params.get("hold_time", 0.05)
        self.seed = params.get("seed", None)

    def _start_noise_effect(self, node_id, min_value, max_value):
        pixel_targets = [(node_id, i) for i in range(8)]

        generator = RandomNoiseGenerator(
            min_value=min_value,
            max_value=max_value,
            hold_time=self.hold_time,
            seed=self.seed
        )

        effect = PixelColorEffect(
            self.table_api,
            generator,
            pixel_targets,
            {},
        )

        self.active_effects[node_id] = effect

    def handle_node_touched(self, node_id):
        self._start_noise_effect(node_id, self.touch_min, self.touch_max)

    def handle_node_untouched(self, node_id):
        self._start_noise_effect(node_id, self.untouch_min, self.untouch_max)

    def loop(self, tick, delta_time):
        for node_id, effect in list(self.active_effects.items()):
            effect.tick(delta_time, tick)
            effect_updates = effect.get_pixel_updates()

            for nid, pixels in effect_updates.items():
                for idx, color in enumerate(pixels):
                    if color is not None:
                        self.table_api.setNodePixel(nid, idx, wrgb_tuple_to_int(color))

        self.table_api.refresh()
