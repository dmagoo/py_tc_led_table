"""
Base class for all parameter generators.

Generators produce values dynamically based on 't'.
Effects can pass 't' explicitly (for precise control) or let the generator manage its own internal t.

All generators also support Python iterator protocol.
- Calling next(generator) will automatically advance using internal stepping.

Developer Tip:
- Always define 'range' and 'step' explicitly when creating generators.
- For simple effects, pass tick or frame count as t.
- For advanced effects, t can come from another generator (e.g., sine wave, easing function).
"""
class BaseGenerator:
    def __init__(self, range, step, **params):
        self.range = range
        self.step = step
        self.params = params
        self.internal_t = 0

    def get_value(self, t=None):
        """Return the generated value. Use external t if provided, otherwise internal stepping."""
        raise NotImplementedError("Subclasses must implement get_value(t=None)")

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_value()

    def reset(self):
        """Reset internal progression (if needed)."""
        self.internal_t = 0
