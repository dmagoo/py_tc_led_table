# CMakeLists.txt for Python bindings

# Ensure pybind11 is available
if(NOT TARGET pybind11::pybind11)
    message(FATAL_ERROR "pybind11 not found. Please ensure TCLEDTABLE_BUILD_PYTHON_BINDINGS is ON and pybind11 is available.")
endif()

# Create the Python binding module
pybind11_add_module(tc_led_table_core
    src/tc_led_table_module.cpp
    src/coordinate_bindings.cpp
    src/config_bindings.cpp
)

# Set target properties
set_target_properties(tc_led_table_core PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    # Output name matches Python import
    OUTPUT_NAME "tc_led_table"
    # Set output directory for development
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/../python
)

# Include directories
target_include_directories(tc_led_table_core PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../src
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/tc_led_table
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/tc_led_table/core
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/tc_led_table/config
    ${CMAKE_CURRENT_SOURCE_DIR}/../src/tc_led_table/api
)

# Link with core library
target_link_libraries(tc_led_table_core PRIVATE
    TCLEDTable::Core
    TCLEDTable_warnings
)

# Compiler-specific settings
target_compile_definitions(tc_led_table_core PRIVATE
    VERSION_INFO="${PROJECT_VERSION}"
)

# Install the module
if(TCLEDTABLE_INSTALL)
    install(TARGETS tc_led_table_core
        LIBRARY DESTINATION python/tc_led_table
        RUNTIME DESTINATION python/tc_led_table
    )
endif()

# Create symlink for development
if(CMAKE_SYSTEM_NAME STREQUAL "Linux" OR CMAKE_SYSTEM_NAME STREQUAL "Darwin")
    add_custom_command(TARGET tc_led_table_core POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E create_symlink
            $<TARGET_FILE:tc_led_table_core>
            ${CMAKE_CURRENT_SOURCE_DIR}/../python/tc_led_table/$<TARGET_FILE_NAME:tc_led_table_core>
        COMMENT "Creating development symlink for Python module"
    )
endif()
