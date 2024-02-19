git submodule add https://github.com/dmagoo/TC_LED_Table.git lib/tc_led_table
git submodule update --init --recursive


Windows:
.\.venv\Scripts\activate
pip install -r requirements.txt

Mac / Linux
source .venv/bin/activate
pip install -r requirements.txt

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
