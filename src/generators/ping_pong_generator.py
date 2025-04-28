from .base_generator import BaseGenerator

class PingPongGenerator(BaseGenerator):
    """
    PingPongGenerator

    Oscillates back and forth between two integer bounds.

    - Accepts either a static range tuple or a range generator.
    - Supports optional step size.
    """
    def __init__(self, range_or_range_generator, step=1, **params):
        super().__init__(**params)
        self.range_source = range_or_range_generator
        self.step = step

    def compute(self, t):
        # Resolve range
        try:
            start, end = self.range_source.get_value(t)
        except AttributeError:
            start, end = self.range_source

        span = end - start
        if span == 0:
            return start

        # Total cycle length (forward + backward)
        cycle = 2 * span
        pos = int(round(t * self.step)) % cycle

        if pos < span:
            return start + pos
        else:
            return end - (pos - span)
