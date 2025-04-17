import time
from EffectRunner import EffectRunner
import os, sys
script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('examples')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))



from ripple import Ripple
from snek import SnekApp
import tc_led_table
from settings import add_controller_config, add_sensor_listener_config

""" A simple script to run the effect runner from the CLI"""

def main():
    # Initialize the API (combines controller and sensor capabilities)
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    print("f")
    print(led_table_config)
    led_table_config = add_sensor_listener_config(led_table_config)
    print("t")
    print(led_table_config)

    # Initialize the table with the enhanced config
    tc_led_table.init(config=led_table_config)
    print(tc_led_table)
    
    # List of effect classes (Ripple and Snek)
    effects = [SnekApp, Ripple]

    # Create an instance of the EffectRunner
    effect_runner = EffectRunner(effects, tc_led_table)

    # Run the effects
    effect_runner.run()

if __name__ == "__main__":
    main()
