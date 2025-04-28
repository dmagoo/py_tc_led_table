"""
BaseGenerator

Abstract base class for all generators.

- get_value(t=None): Returns the computed value.
  - If t is not provided, internal_t is used and incremented automatically.
- compute(t): Child classes must implement this to define behavior.
- reset(): Resets internal_t and output_count to 0.
- Supports iterator protocol (__iter__, __next__).
  - Raises StopIteration if is_done(t) or max_len is reached.

Design goals:
- Keep all progression logic centralized.
- Child classes only implement compute(t) with no side effects.
- Consistent output for a given t is strongly recommended.
"""

class BaseGenerator:
    def __init__(self, max_len=None, **params):
        self.params = params
        self.internal_t = 0
        self.max_len = max_len
        self.output_count = 0

    def get_value(self, t=None):
        if t is None:
            t = self.internal_t
            self.internal_t += 1
        return self.compute(t)

    def compute(self, t):
        raise NotImplementedError("Subclasses must implement compute(t)")

    def is_done(self, t):
        if self.max_len is not None and self.output_count >= self.max_len:
            return True
        return False

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_len is not None and self.output_count >= self.max_len:
            raise StopIteration

        t = self.internal_t
        if self.is_done(t):
            raise StopIteration

        self.internal_t += 1
        self.output_count += 1
        return self.compute(t)

    def reset(self):
        self.internal_t = 0
        self.output_count = 0
