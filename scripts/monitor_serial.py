#!/usr/bin/env python3
# NOTE. This requires usb privileges:
# as the user running the program, do:
# sudo usermod -aG dialout $USER
import json
import os
import sys
import serial
import serial.tools.list_ports
import threading
import time

script_dir = os.path.dirname(__file__)
sys.path.append('src')
sys.path.append('src/pygame')
sys.path.append('src/config')
sys.path.append(os.path.abspath('lib/tc_led_table/python_bindings/Release'))


import platform

bindings_dir = 'lib/tc_led_table/python_bindings'
if platform.system() == 'Windows':
    bindings_dir = os.path.join(bindings_dir, 'Release')

sys.path.append(os.path.abspath(bindings_dir))

import tc_led_table, tc_sensor_transmitter
from settings import add_sensor_transmit_config, add_monitor_config


EXPECTED_CLUSTER_COUNT = 4
active_cluster_ids = set()
unconfigured_ports = []

led_table_config = add_monitor_config(tc_led_table.LedTableConfig())
tc_led_table.init(config=led_table_config)
sensor_config = add_sensor_transmit_config(tc_led_table.LedTableConfig())

sensor_config.mqttConfig.clientId = 'pySerialMonitor'
tc_sensor_transmitter.init(config=sensor_config)

sensor_api = tc_sensor_transmitter

def build_config(cluster_id):
    return json.dumps({
        "clusterId": cluster_id,
        "nodes": [
            # TODO: Populate node layout for this cluster
        ]
    })

def handle_message(port_path, line):
    try:
        data = json.loads(line)
        event = data.get("eventType")

        if event == "config_status":
            status = data.get("status")
            cluster_id = data.get("clusterId")

            if status == "config_missing":
                if len(active_cluster_ids) < EXPECTED_CLUSTER_COUNT:
                    next_id = next(i for i in range(EXPECTED_CLUSTER_COUNT) if i not in active_cluster_ids)
                    config_json = build_config(next_id)
                    with serial.Serial(port_path, 115200, timeout=2) as ser:
                        ser.write(config_json.encode('utf-8'))
                        ser.write(b'\n')
                        active_cluster_ids.add(next_id)
                        print(f"Assigned clusterId {next_id} to {port_path}")
                else:
                    print(f"[ERROR] All clusterIds in use. Ignoring device on {port_path}")
            elif status == "config_loaded" or status == "config_received":
                if cluster_id in active_cluster_ids:
                    print(f"[WARNING] Duplicate clusterId {cluster_id} from {port_path}. Ignored.")
                else:
                    active_cluster_ids.add(cluster_id)
                    print(f"Device on {port_path} confirmed with clusterId {cluster_id}")

        elif event == "touch_event":  # or event == "periodic_touch_status":
            print(data)
            for item in data.get("sensorData", []):
                node_id = item["nodeId"]
                touched = item["touched"]
                value = 100 if touched else 0
                sensor_api.sendTouchSensorEvent(node_id, value, touched)
    except Exception as e:
        print(f"[ERROR] Failed to handle message from {port_path}: {e}")

def get_connected_devices():
    # List all connected serial devices
    ports = serial.tools.list_ports.comports()
    connected_devices = []
    
    for port in ports:
        connected_devices.append(port.device)
    
    return connected_devices

def monitor_device(port_path):
    try:
        with serial.Serial(port_path, 115200, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    handle_message(port_path, line)
    except Exception as e:
        print(f"[ERROR] Monitoring failed for {port_path}: {e}")

def monitor_all_devices():
    # Monitor all connected devices and report status
    connected_devices = get_connected_devices()
    if len(connected_devices) == 0:
        print("[ERROR] No devices connected.")
    else:
        print(f"Connected devices: {connected_devices}")
        # Start monitoring the devices in separate threads
        threads = []
        for port in connected_devices:
            t = threading.Thread(target=monitor_device, args=(port,))
            t.daemon = True
            t.start()
            threads.append(t)
        # Keep the main thread alive
        while True:
            time.sleep(60)

def main():
    monitor_all_devices()

if __name__ == "__main__":
    main()
