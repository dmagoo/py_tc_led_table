# effect_registry.py
# Lives next to EffectRunner. Used by both runner and Flask.
import sys
sys.path.append('examples')

from ripple import Ripple
from snek import SnekApp
from statusPulse import StatusPulse

EFFECT_REGISTRY = {
    "Ripple": {
        "class": Ripple,
        "params": {
            "speed": {
                "type": "float",
                "default": 1.0,
                "min": 0.1,
                "max": 5.0,
                "widget": "slider"
            },
            "color": {
                "type": "color",
                "default": [255, 0, 0, 0]
            }
        }
    },
    "SnekApp": {
        "class": SnekApp,
        "params": {
            "interval": {
                "type": "int",
                "default": 500,
                "min": 100,
                "max": 1000,
                "widget": "slider"
            },
            "mode": {
                "type": "enum",
                "options": ["normal", "chaotic", "reverse"],
                "default": "normal"
            }
        }
    },
    "StatusPulse": {
        "class": StatusPulse,
        "params": {
            "speed": {
                "type": "float",
                "default": 1.0,
                "min": 0.1,
                "max": 5.0,
                "widget": "slider"
            },
            "color": {
                "type": "color",
                "default": [255, 0, 0, 0]
            }
        }
    },

}
