import os
import configparser
import sys

# Load configuration from a file
config = configparser.ConfigParser()
config_file = 'config.ini'
if os.path.exists(config_file):
    config.read(config_file)

def get_config_value(section, option, env_var_name, default=None):
    env_value = os.getenv(env_var_name)
    if env_value:
        return env_value

    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)

    if config.has_section("Default") and config.has_option("Default", option):
        return config.get("Default", option)

    if default is not None:
        return default

    raise ValueError(f"Configuration for {section}.{option} not found in environment, section, or [Default]")


def add_monitor_config(led_table_config):
    led_table_config.enableArtnetMessaging=True 
    return led_table_config

def add_controller_config(led_table_config):
    # this app is will use artnet isntead
    led_table_config.enableArtnetMessaging=True 

    broker_address = get_config_value('Artnet', 'broker_address', 'BROKER_ADDRESS')
    print(f"Artnet Broker Address: {broker_address}")
    led_table_config.artnetConfig.brokerAddress=broker_address


    return led_table_config
