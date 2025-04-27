import random
from .base_generator import BaseGenerator

class RandomNoiseGenerator(BaseGenerator):
    """
    RandomNoiseGenerator

    - Returns random values (scalar or tuple) based on min_value and max_value.
    - Hold_time defines how long (in t units) a value is held before refreshing.
    - Guarantees consistent output for the same t input.
    - Optional seed for reproducible or fresh runs.
    """

    def __init__(self, min_value=0, max_value=255, hold_time=1, seed=None, **params):
        super().__init__(**params)
        self.min_value = min_value
        self.max_value = max_value
        self.hold_time = hold_time

        if isinstance(self.min_value, tuple) != isinstance(self.max_value, tuple):
            raise ValueError("min_value and max_value must both be scalar or both be tuple")
        if isinstance(self.min_value, tuple) and len(self.min_value) != len(self.max_value):
            raise ValueError("min_value and max_value tuples must be the same length")

        self.session_seed = seed if seed is not None else random.randint(0, 1_000_000)

    def compute(self, t):
        slot = int(t / self.hold_time)
        final_seed = self.session_seed + slot
        random.seed(final_seed)

        if isinstance(self.min_value, tuple):
            return tuple(
                random.randint(min_v, max_v)
                for min_v, max_v in zip(self.min_value, self.max_value)
            )
        else:
            return random.randint(self.min_value, self.max_value)
