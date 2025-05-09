cmake_minimum_required(VERSION 3.5)
project(LedTableApiBindings)
set(pybind11_DIR "${CMAKE_SOURCE_DIR}/lib/pybind11/share/cmake/pybind11")

pybind11_add_module(tc_led_table 
    tc_led_table_module.cpp
    coordinate_bindings.cpp
    config_bindings.cpp
)

set_target_properties(tc_led_table PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python_bindings
)

target_include_directories(tc_led_table PRIVATE
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}/src/core
    ${CMAKE_SOURCE_DIR}/src/config
    ${CMAKE_SOURCE_DIR}/src/api
)


# Link the Python bindings module with the LedTableApi library
target_link_libraries(tc_led_table PRIVATE 
    LedTableApi 
    $<$<PLATFORM_ID:Windows>:WinLib ${ARTNET_LIBRARIES} ws2_32>
    $<$<NOT:$<PLATFORM_ID:Windows>>:${LIBARTNET_LIBRARY}>
)

# Link the main C++ project library
target_link_libraries(tc_led_table PRIVATE LedTableApi ${Python_LIBRARIES})

#pybind11_add_module(tc_sensor_transmitter
#    sensor_bindings.cpp
#    config_bindings.cpp
#)

#set_target_properties(tc_sensor_transmitter PROPERTIES
#    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/python_bindings
#)

#target_include_directories(tc_sensor_transmitter PRIVATE
#    ${CMAKE_SOURCE_DIR}/src
#    ${CMAKE_SOURCE_DIR}/src/core
#    ${CMAKE_SOURCE_DIR}/src/config
#)


# Link the Python bindings module with the LedTableApi library
#target_link_libraries(tc_sensor_transmitter PRIVATE 
#    LedTableApi 
#    $<$<PLATFORM_ID:Windows>:WinLib ${PAHO_MQTT_C_LIBRARIES} ${PAHO_MQTT_CPP_LIBRARIES}  ws2_32>
#    $<$<NOT:$<PLATFORM_ID:Windows>>:PahoMqttCpp::paho-mqttpp3-static>
#)

# Link the main C++ project library
#target_link_libraries(tc_sensor_transmitter PRIVATE LedTableApi ${Python_LIBRARIES})
