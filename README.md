git submodule add https://github.com/dmagoo/TC_LED_Table.git lib/tc_led_table
git submodule update --init --recursive


Windows:
.\.venv\Scripts\activate
pip install -r requirements.txt


Mac / Linux
source .venv/bin/activate
pip install -r requirements.txt

Add path to venv:
echo "/home/tcledtable/projects/py_tc_led_table/src" > .venv/lib/python3.11/site-packages/project_paths.pth
echo "/home/tcledtable/projects/py_tc_led_table/examples" >> .venv/lib/python3.11/site-packages/project_paths.pth


update config.ini to include mqtt broker ip address, if needed

# to update and build bindings
git submodule update --recursive --remote
cd lib\tc_led_table
mkdir build
cd build
cmake ..
#cmake build . --config Release
cmake --build . --config Release  --target tc_led_table # to control the table
cmake --build . --config Release  --target tc_sensor_transmitter # to send sensor data to the controller


#### MQTT Messages
"ledtable/sensor/touch"
touch topic: this uses a very compressed data packet via nanopb
likely something we can iterate away from, as touches are pretty
infrequent

SensorEventData {
  event_type: touch_event / periodic
    sensor_data {
      node_id
      touched // bool
      // deprecated props, for analog sensors
      current_value // value of analog sensor deprecated
      threshold_off // this or lower is "off"
      threshold_on// this or higher is "on"
}
}

#all cluster commands are deprecated. we no longer us MQTT / nanopb for pixel data
# this all now gos out over artnet, and not to the cluster controllers