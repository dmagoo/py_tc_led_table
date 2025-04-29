# src/pygame/models/node.py
from utils import perceptual_display_color

NODE_COLOR_DEFAULT = (33,33,33)


class Node:
    def __init__(self, id, coord, radius, color=NODE_COLOR_DEFAULT, touch_threshold=50):
        self.id = id
        self.cartesian_2d_coord = coord
        self.radius = radius
        self.color = color
        self._colors = [self._pad_color(color) for _ in range(8)]
        self.touch_threshold = touch_threshold
        self.touch_value = 0

    @staticmethod
    def _pad_color(color):
        """Pad the color tuple with a default W value if necessary."""
        return color if len(color) == 4 else  (0,) + color

    @property
    def colors(self):
        return self._colors
    @property
    def touched(self):
        return self.touch_value >= self.touch_threshold

    @colors.setter
    def colors(self, value):
        # Ensure each color tuple in the list has 4 elements, padding with a default W value if necessary
        #self._colors = [(c if len(c) == 4 else (0,) + c) for c in value]
        self._colors = [(c if len(c) == 4 else self._pad_color(c)) for c in value]

    @property
    def colors_rgb(self):
        return [color[1:4] for color in self._colors]

    @property
    def colors_lcd_display(self):
        """
        Gamma-encoded RGB colors for screen display.
        Extracts RGB from internal WRGB tuples and maps each through gamma correction.
        """
        return [perceptual_display_color(c[1:4]) for c in self._colors]
