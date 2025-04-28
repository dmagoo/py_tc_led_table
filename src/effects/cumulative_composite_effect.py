class CumulativeCompositeEffect(BaseCompositeEffect):
    """
    CumulativeCompositeEffect

    Combines pixel updates from all child effects.

    - Later effects overwrite earlier ones if they update the same pixel.
    - Optionally fades out older pixel updates after max_age seconds.
    """

    def __init__(self, table_api, child_effects, max_age=None, **params):
        super().__init__(table_api, child_effects, **params)
        self.max_age = max_age
        self.history = []  # List of (timestamp, updates)

    def tick(self, delta_time, tick):
        super().tick(delta_time, tick)

        # Capture the current frame of updates
        frame_updates = {}
        for effect in self.child_effects:
            updates = effect.get_pixel_updates()
            for node_id, pixels in updates.items():
                if node_id not in frame_updates:
                    frame_updates[node_id] = [None] * 8
                for idx, color in enumerate(pixels):
                    if color is not None:
                        frame_updates[node_id][idx] = color

        if frame_updates:
            self.history.append((self.elapsed_time, frame_updates))

        # Prune old frames if max_age is set
        if self.max_age is not None:
            cutoff = self.elapsed_time - self.max_age
            self.history = [(t, updates) for (t, updates) in self.history if t >= cutoff]

    def get_pixel_updates(self):
        node_updates = {}

        for _, updates in self.history:
            for node_id, pixels in updates.items():
                if node_id not in node_updates:
                    node_updates[node_id] = [None] * 8
                for idx, color in enumerate(pixels):
                    if color is not None:
                        node_updates[node_id][idx] = color

        return node_updates
