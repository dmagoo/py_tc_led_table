"""
Base class for all effects.

Effects manage their own lifecycle, use generators for parameters,
and output pixel updates each frame.

Effects can finish automatically using an optional stop_condition,
or can set done manually inside their own logic.

Developer Tip:
- Apps should call tick() every update cycle.
- Apps should check the done property to know if an effect has completed.
"""

class BaseEffect:
    def __init__(self, table_api, stop_condition=None, **params):
        self.table_api = table_api
        self.params = params
        self.stop_condition = stop_condition
        self.done = False
        self.elapsed_time = 0.0
        self.reset(params)

    def reset(self, params=None, stop_condition=None):
        """Reset the effect with optional new parameters."""
        if params:
            self.params.update(params)
        if stop_condition is not None:
            self.stop_condition = stop_condition
        self.done = False
        self.internal_tick = 0
        self.elapsed_time = 0.0

    def tick(self, delta_time, tick):
        """Advance the effect's state."""
        self.internal_tick += 1
        self.elapsed_time += delta_time
        if self.stop_condition:
            self.done = self.handle_stop_condition()

    def handle_stop_condition(self):
        """Evaluate the stop condition. Can be overridden by subclasses for custom behavior."""
        return self.stop_condition(self)

    def get_pixel_updates(self):
        """Return a list or dict of pixel updates to apply. Must be overridden."""
        raise NotImplementedError("Subclasses must implement get_pixel_updates()")
