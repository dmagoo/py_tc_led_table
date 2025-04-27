from .base_generator import BaseGenerator

class StableValueGenerator(BaseGenerator):
    """
    A generator that always returns the same static value, regardless of t.
    """
    def __init__(self, value):
        super().__init__(range=(value, value), step=0)
        self.value = value

    def get_value(self, t=None):
        return self.value
