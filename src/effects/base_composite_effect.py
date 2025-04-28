from .base_effect import BaseEffect

class BaseCompositeEffect(BaseEffect):
    """
    BaseCompositeEffect

    Manages multiple child effects together.

    - Calls tick() on all child effects.
    - Collects and combines pixel updates.
    - Subclasses define how merging is handled.
    """

    def __init__(self, table_api, child_effects, **params):
        super().__init__(table_api, **params)
        self.child_effects = child_effects

    def tick(self, delta_time, tick):
        self.internal_tick += 1
        self.elapsed_time += delta_time
        for effect in self.child_effects:
            effect.tick(delta_time, tick)

    def get_pixel_updates(self):
        raise NotImplementedError("Subclasses must implement get_pixel_updates()")
