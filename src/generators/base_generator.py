"""
BaseGenerator

Abstract base class for all generators.

- get_value(t=None): Returns the computed value.
  - If t is not provided, internal_t is used and incremented automatically.
- compute(t): Child classes must implement this to define behavior.
- reset(): Resets internal_t to 0.
- Supports iterator protocol (__iter__, __next__).

Design goal:
- Keep all progression logic centralized.
- Child classes only implement compute(t) with no side effects.
"""

class BaseGenerator:
    def __init__(self, **params):
        self.params = params
        self.internal_t = 0

    def get_value(self, t=None):
        if t is None:
            t = self.internal_t
            self.internal_t += 1
        return self.compute(t)

    def compute(self, t):
        raise NotImplementedError("Subclasses must implement compute(t)")

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_value()

    def reset(self):
        self.internal_t = 0
