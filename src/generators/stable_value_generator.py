from .base_generator import BaseGenerator

class StableValueGenerator(BaseGenerator):
    """
    A generator that always returns the same static value.
    Optionally supports a duration after which it is considered done.
    """
    def __init__(self, value, duration=None):
        super().__init__()
        self.value = value
        self.duration = duration

    def compute(self, t):
        return self.value

    def is_done(self, t):
        if self.duration is None:
            return False
        return t >= self.duration
