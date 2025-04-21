# manage_effects.py
# Systemd-launched script to run the EffectRunner

import time
import os, sys
from EffectRunner import EffectRunner

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('examples')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)
    tc_led_table.init(config=led_table_config)

    effect_runner = EffectRunner(tc_led_table)
    effect_runner.run()

if __name__ == "__main__":
    main()
