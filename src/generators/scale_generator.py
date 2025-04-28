from .base_generator import BaseGenerator

class ScaleGenerator(BaseGenerator):
    """
    ScaleGenerator

    Multiplies the input t by a fixed scale factor.

    - Supports scalars and tuples.
    - Optimizes by determining type on first call.
    """

    def __init__(self, scale, **params):
        super().__init__(**params)
        self.scale = scale
        self._do_compute = self._determine_compute

    def _determine_compute(self, t):
        if isinstance(t, tuple):
            self._do_compute = self._tuple_wise
        else:
            self._do_compute = self._scalar_wise
        return self._do_compute(t)

    def _tuple_wise(self, t):
        return tuple(x * self.scale for x in t)

    def _scalar_wise(self, t):
        return t * self.scale

    def compute(self, t):
        return self._do_compute(t)
