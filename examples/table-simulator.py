"""
This example file shows how to create an TCTable simulator
It uses python bindings to the table api update the local model,
But uses a local artnet implementation to receive the pixel data
From the controller. It also uses the Sensor Transmitter bindings to
Simulate touch events, to send to the api over mqtt
"""

import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append('src/artnet')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import tc_led_table, tc_sensor_transmitter

from settings import add_monitor_config, add_sensor_transmit_config
from TableSimulator import TableSimulator

def main():
    try:
        led_table_config = add_monitor_config(tc_led_table.LedTableConfig())
        tc_led_table.init(config=led_table_config)

        led_table_sensor_config = add_sensor_transmit_config(tc_led_table.LedTableConfig())
        led_table_sensor_config.mqttConfig.clientId = 'pyTableSimulator'
        tc_sensor_transmitter.init(config=led_table_sensor_config)

        app = TableSimulator(tc_led_table, tc_sensor_transmitter)
        app.run()  # Start the app's main loop

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
