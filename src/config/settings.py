import os
import configparser
import sys

# Load configuration from a file
config = configparser.ConfigParser()
config_file = 'config.ini'
if os.path.exists(config_file):
    config.read(config_file)

# Function to get configuration value
def get_config_value(section, option, env_var_name, default=None):
    env_value = os.getenv(env_var_name)
    if env_value:
        return env_value

    if config.has_section(section) and config.has_option(section, option):
        return config.get(section, option)

    if default:
        return default

    raise ValueError(f"Configuration for {section}.{option} not found in environment variables or config file")

def add_monitor_config(led_table_config):
    broker_address = get_config_value('MQTT', 'broker_address', 'BROKER_ADDRESS')      
    print(f"Broker Address: {broker_address}")

    led_table_config.enableMQTTMessaging=False 
    led_table_config.enableArtnetMessaging=True 
    led_table_config.mqttConfig.brokerAddress=broker_address 
    led_table_config.mqttConfig.clientId = 'pyMonitor'
    return led_table_config

def add_controller_config(led_table_config):
    # this app is will use artnet isntead
    led_table_config.enableMQTTMessaging=False 
    led_table_config.enableArtnetMessaging=True 
    return led_table_config

def add_sensor_listener_config(led_table_config):
    broker_address = get_config_value('MQTT', 'broker_address', 'BROKER_ADDRESS')      
    print(f"Broker Address: {broker_address}")

    #this app will listen for touch sensors
    led_table_config.enableMQTTSubscriptions=True
    led_table_config.mqttConfig.brokerAddress=broker_address
    return led_table_config

def add_sensor_transmit_config(led_table_config):
    broker_address = get_config_value('MQTT', 'broker_address', 'BROKER_ADDRESS')      
    print(f"Broker Address: {broker_address}")

    led_table_config.enableMQTTMessaging=False
    led_table_config.enableMQTTSubscriptions=True
    led_table_config.enableArtnetMessaging=True 
    led_table_config.mqttConfig.brokerAddress=broker_address
    led_table_config.mqttConfig.clientId = 'pySensorTransmitter'
    return led_table_config