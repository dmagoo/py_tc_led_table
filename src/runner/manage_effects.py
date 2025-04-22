# manage_effects.py
# Systemd-launched script to run the EffectRunner

import time
import os, sys
from EffectRunner import EffectRunner

import bootstrap_bindings
from bootstrap_bindings import setup_paths
setup_paths()

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))

import tc_led_table
from settings import add_controller_config, add_sensor_listener_config, get_config_value
from communication.mqtt_client import setup_mqtt_client
from communication.message_manager import MessageManager

def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    led_table_config = add_sensor_listener_config(led_table_config)
    tc_led_table.init(config=led_table_config)

    broker = get_config_value("EffectRunner", "mqtt_broker_address", "MQTT_BROKER_ADDRESS")
    client_id = get_config_value("EffectRunner", "mqtt_client_id", "MQTT_CLIENT_ID")

    mqtt_client = setup_mqtt_client(broker_address=broker, client_id=client_id)
    message_manager = MessageManager(mqtt_client)

    effect_runner = EffectRunner(tc_led_table, message_manager)
    effect_runner.run()

if __name__ == "__main__":
    main()
