from .base_generator import BaseGenerator

class TweenGenerator(BaseGenerator):
    """
    TweenGenerator

    Linearly interpolates from start to end over a fixed duration.
    Clamps at start and end (no wrapping).
    """
    def __init__(self, range, duration, **params):
        super().__init__(**params)
        self.range = range
        self.duration = duration

    def compute(self, t):
        start, end = self.range
        normalized_t = max(0.0, min(t / self.duration, 1.0))

        if isinstance(start, tuple):
            return tuple(int(self._lerp(s, e, normalized_t)) for s, e in zip(start, end))
        else:
            return int(self._lerp(start, end, normalized_t))

    def _lerp(self, start, end, t_normalized):
        return start + (end - start) * t_normalized

    def is_done(self, t):
        return t >= self.duration
