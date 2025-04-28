from .base_effect import BaseEffect

class ChainEffect(BaseEffect):
    """
    ChainEffect

    Runs a sequence of effects one after another.
    Only the active effect is ticked at any time.
    """

    def __init__(self, table_api, effects, stop_condition=None, **params):
        super().__init__(table_api, params, stop_condition)
        self.effects = effects  # List of effect instances
        self.current_index = 0
        self.latest_pixel_updates = {}

    def tick(self, delta_time, tick):
        super().tick(delta_time, tick)

        if self.current_index >= len(self.effects):
            self.done = True
            return

        current_effect = self.effects[self.current_index]
        current_effect.tick(delta_time, tick)

        # Capture pixel updates immediately after ticking
        self.latest_pixel_updates = current_effect.get_pixel_updates()

        if current_effect.done:
            self.current_index += 1

            if self.current_index >= len(self.effects):
                self.done = True

    def get_pixel_updates(self):
        return self.latest_pixel_updates
