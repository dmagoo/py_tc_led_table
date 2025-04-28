from .base_generator import BaseGenerator
"""
CompositeGenerator

Chains multiple generators together.

- Takes multiple generators as input.
- Passes the input t through each generator in sequence.
- Each generator’s output becomes the next generator’s input.
- Final output is produced after all generators have processed.

Design goals:
- Allow flexible generator composition without changing child classes.
- Maintain consistency with BaseGenerator behavior.
"""

class CompositeGenerator(BaseGenerator):
    def __init__(self, *generators, **params):
        super().__init__(**params)
        self.generators = generators

    def compute(self, t):
        value = t
        for gen in self.generators:
            value = gen.get_value(value)
        return value
