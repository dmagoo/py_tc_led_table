from math import sin, pi
from .base_generator import BaseGenerator

class SineGenerator(BaseGenerator):
    """
    SineGenerator

    Outputs a normalized sine wave (0 to 1) based on input t.
    
    - frequency: number of full cycles per unit t
    - phase: phase shift in units of t
    - No stopping; oscillates infinitely.
    """
    def __init__(self, frequency=1.0, phase=0.0, **params):
        super().__init__(**params)
        self.frequency = frequency
        self.phase = phase

    def compute(self, t):
        angle = 2 * pi * self.frequency * (t + self.phase)
        return 0.5 * (sin(angle) + 1.0)  # Normalize from [-1, 1] → [0, 1]
