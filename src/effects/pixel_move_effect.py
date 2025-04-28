from .base_effect import BaseEffect

class PixelMoveEffect(BaseEffect):
    """
    PixelMoveEffect

    Moves a pixel across a list of (node_id, pixel_index) positions.

    - Uses position_index_generator to select which position is active.
    - Optionally uses color_generator to set pixel color.
    - Optionally erases the previously lit pixel each tick.
    """

    def __init__(self, table_api, pixel_positions, position_index_generator, color_generator=None, erase_last_pixel=False, **params):
        super().__init__(table_api, **params)
        self.pixel_positions = pixel_positions
        self.position_index_generator = position_index_generator
        self.color_generator = color_generator
        self.erase_last_pixel = erase_last_pixel
        self.current_color = (255, 255, 255, 255)  # Default to white
        self.active_update = None
        self.last_update = None

    def tick(self, delta_time, tick):
        self.internal_tick += 1
        self.elapsed_time += delta_time

        index = int(self.position_index_generator.get_value(self.elapsed_time))
        index = max(0, min(index, len(self.pixel_positions) - 1))

        node_id, pixel_index = self.pixel_positions[index]

        if self.color_generator:
            raw_color = self.color_generator.get_value(self.elapsed_time)
            if isinstance(raw_color, tuple):
                self.current_color = tuple(int(v) for v in raw_color)
            else:
                self.current_color = int(raw_color)

        # Save old and new active pixel
        self.last_update = self.active_update
        self.active_update = (node_id, pixel_index)

    def get_pixel_updates(self):
        node_updates = {}

        if self.erase_last_pixel and self.last_update is not None:
            last_nid, last_idx = self.last_update
            if last_nid not in node_updates:
                node_updates[last_nid] = [None] * 8
            node_updates[last_nid][last_idx] = (0, 0, 0, 0)  # Black out

        if self.active_update is not None:
            nid, idx = self.active_update
            if nid not in node_updates:
                node_updates[nid] = [None] * 8
            node_updates[nid][idx] = self.current_color

        return node_updates
