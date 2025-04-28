import time
from utils import wrgb_tuple_to_int
from effects.chain_effect import ChainEffect
from effects.pixel_color_effect import PixelColorEffect
from generators.stable_value_generator import StableValueGenerator
from generators.tween_generator import TweenGenerator
from apps.AppBase import AppBase

class TestApp(AppBase):
    def __init__(self, table_api, params={}):
        super().__init__(table_api, params)
        self.active_effects = {}

        # App params
        self.base_color = params.get("flash_color", (255, 255, 255, 255))
        self.fade_target = params.get("fade_target", (0, 0, 0, 0))
        self.total_duration = params.get("total_duration", 1)  # seconds
        self.flash_fraction = params.get("flash_fraction", 0.68)  # 68% flash, 32% fade

    def handle_node_touched(self, node_id):
        if node_id in self.active_effects:
            return

        pixel_targets = [(node_id, i) for i in range(8)]

        flash_duration = self.total_duration * self.flash_fraction
        fade_duration = self.total_duration * (1 - self.flash_fraction)

        # Flash part
        flash_gen = StableValueGenerator(self.base_color, duration=flash_duration)
        flash_effect = PixelColorEffect(
            self.table_api,
            flash_gen,
            pixel_targets,
            {}
        )

        # Fade part
        fade_gen = TweenGenerator(
            range=(self.base_color, self.fade_target),
            duration=fade_duration
        )
        fade_effect = PixelColorEffect(
            self.table_api,
            {},
            fade_gen,
            pixel_targets
        )

        chain = ChainEffect(self.table_api, {}, [flash_effect, fade_effect])
        self.active_effects[node_id] = chain

    def handle_node_untouched(self, node_id):
        pass

    def loop(self, tick, delta_time):
        for node_id, effect in list(self.active_effects.items()):
            effect.tick(delta_time, tick)
            effect_updates = effect.get_pixel_updates()

            for nid, pixels in effect_updates.items():
                for idx, color in enumerate(pixels):
                    if color is not None:
                        self.table_api.setNodePixel(nid, idx, wrgb_tuple_to_int(color))
            
            if effect.done:
                del self.active_effects[node_id]
                
        self.table_api.refresh()
