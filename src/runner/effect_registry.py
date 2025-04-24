# effect_registry.py
# Lives next to EffectRunner. Used by both runner and Flask.
import sys
sys.path.append('examples')

from ripple import Ripple
from snek import SnekApp
from statusPulse import StatusPulse
from incrementalFill import IncrementalFill
from wipe import Wipe
from testNode import TestNode
from connectNodes import ConnectNodes

EFFECT_REGISTRY = {
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
                "default": [10, 10, 20, 100]
            }
        }
    },
    "Ripple": {
        "class": Ripple,
        "params": {
            "speed": {
                "type": "float",
                "default": 10,
                "min": 0.1,
                "max": 5.0,
                "widget": "slider"
            },
            "reach": {
                "type": "float",
                "default": 3,
                "min": 1.0,
                "max": 7,
                "widget": "slider"
            },
            "color": {
                "type": "color",
                "default": [0, 66, 11, 77]
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
    "ConnectNodes": {
        "class": ConnectNodes,
        "params": {
            "color": {
                "type": "color",
                "default": [10, 100, 10, 100]
            }
        }
    },
    "Fill": {
        "class": IncrementalFill,
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
                "default": [0, 66, 11, 77]
            }
        }
    },
    "Wipe": {
        "class": Wipe,
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
                "default": [0, 66, 11, 77]
            }
        }
    },
    "TouchTest": {
        "class": TestNode,
        "params": {
            "color": {
                "type": "color",
                "default": [10, 100, 10, 100]
            }
        }
    }
}
