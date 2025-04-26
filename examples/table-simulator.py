"""
This example file shows how to create an TCTable simulator
It uses python bindings to the table api update the local model,
But uses a local artnet implementation to receive the pixel data
From the controller.
"""

import os
import sys
from bootstrap import apply
apply()

import tc_led_table

from settings import add_monitor_config, get_config_value
from TableSimulator import TableSimulator
from communication.mqtt_client import setup_mqtt_client

def main():
    try:
        broker = get_config_value("TableSimulator", "mqtt_broker_address", "MQTT_BROKER_ADDRESS")
        client_id = get_config_value("TableSimulator", "mqtt_client_id", "MQTT_CLIENT_ID")
        mqtt_client = setup_mqtt_client(broker_address=broker, client_id=client_id)

        led_table_config = add_monitor_config(tc_led_table.LedTableConfig())
        tc_led_table.init(config=led_table_config)

        app = TableSimulator(tc_led_table, mqtt_client)
        app.run()  # Start the app's main loop

    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
