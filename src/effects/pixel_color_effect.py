from .base_effect import BaseEffect

class PixelColorEffect(BaseEffect):
    """
    PixelColorEffect

    Colors a fixed set of (node_id, pixel_index) targets based on a color_generator.
    Each tick, all targeted pixels are updated together to the generated color.

    - Uses elapsed_time (seconds) as input to the color_generator.
    - Automatically stops if the color_generator reports done.
    """

    def __init__(self, table_api, color_generator, pixel_targets, **params):
        super().__init__(table_api, **params)
        self.color_generator = color_generator
        self.pixel_targets = pixel_targets
        self.current_color = None

    def tick(self, delta_time, tick):
        self.internal_tick += 1
        self.elapsed_time += delta_time

        # Check if color_generator reports done at this elapsed time
        if hasattr(self.color_generator, 'is_done') and self.color_generator.is_done(self.elapsed_time):
            # Force exact final value
            final_value = self.color_generator.get_value(t=self.color_generator.duration)
            self._set_color(final_value)
            self.done = True
        else:
            raw_value = self.color_generator.get_value(t=self.elapsed_time)
            self._set_color(raw_value)

    def _set_color(self, raw_value):
        if isinstance(raw_value, tuple):
            self.current_color = tuple(int(v) for v in raw_value)
        else:
            self.current_color = int(raw_value)

    def get_pixel_updates(self):
        node_updates = {}
        for node_id, pixel_index in self.pixel_targets:
            if node_id not in node_updates:
                node_updates[node_id] = [None] * 8
            node_updates[node_id][pixel_index] = self.current_color
        return node_updates
