# Dependencies management for TCLEDTable project

include(FetchContent)

# Set common options for all external projects
set(FETCHCONTENT_QUIET ON)

# Create warnings interface library first (needed for compiler settings)
if(NOT TARGET TCLEDTable_warnings)
    add_library(TCLEDTable_warnings INTERFACE)
endif()

# Function to add external dependencies
function(add_external_dependency name)
    set(oneValueArgs GIT_REPOSITORY GIT_TAG)
    set(multiValueArgs CMAKE_ARGS)
    cmake_parse_arguments(DEP "" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
    
    FetchContent_Declare(
        ${name}
        GIT_REPOSITORY ${DEP_GIT_REPOSITORY}
        GIT_TAG ${DEP_GIT_TAG}
        GIT_SHALLOW TRUE
    )
    
    # Set any custom CMAKE arguments
    foreach(arg ${DEP_CMAKE_ARGS})
        set(${arg} ON CACHE BOOL "" FORCE)
    endforeach()
    
    FetchContent_MakeAvailable(${name})
endfunction()

# ============================================================================
# CLI11 - Command Line Interface Library
# ============================================================================
add_external_dependency(CLI11
    GIT_REPOSITORY https://github.com/CLIUtils/CLI11.git
    GIT_TAG v2.4.1
    CMAKE_ARGS
        CLI11_BUILD_TESTS=OFF
        CLI11_BUILD_EXAMPLES=OFF
        CLI11_BUILD_DOCS=OFF
)

# ============================================================================
# Unity - Unit Testing Framework 
# ============================================================================
if(TCLEDTABLE_BUILD_TESTS)
    add_external_dependency(Unity
        GIT_REPOSITORY https://github.com/ThrowTheSwitch/Unity.git
        GIT_TAG v2.5.2
    )
endif()

# ============================================================================
# pybind11 - Python Bindings
# ============================================================================
if(TCLEDTABLE_BUILD_PYTHON_BINDINGS)
    # Set pybind11 options before fetching
    set(PYBIND11_TEST OFF CACHE BOOL "Disable pybind11 tests")
    set(PYBIND11_INSTALL OFF CACHE BOOL "Disable pybind11 install")
    
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG v2.12.0  # Latest stable version
        GIT_SHALLOW TRUE
        GIT_PROGRESS TRUE
    )
    
    FetchContent_MakeAvailable(pybind11)
    
    # Verify pybind11 was successfully fetched
    if(NOT TARGET pybind11::headers)
        message(FATAL_ERROR "pybind11 failed to load. Please check your internet connection.")
    endif()
endif()

# ============================================================================
# System Dependencies
# ============================================================================

# Art-Net Library
if(WIN32)
    set(LIBARTNET_ROOT "C:/DevTools/libartnet" CACHE PATH "Path to libartnet")
    
    if(EXISTS "${LIBARTNET_ROOT}")
        add_library(LibArtNet::LibArtNet STATIC IMPORTED)
        set_target_properties(LibArtNet::LibArtNet PROPERTIES
            IMPORTED_LOCATION "${LIBARTNET_ROOT}/msvc/libartnet/x64/Release/libartnet.lib"
            INTERFACE_INCLUDE_DIRECTORIES "${LIBARTNET_ROOT};${LIBARTNET_ROOT}/artnet"
        )
    else()
        message(WARNING "libartnet not found on Windows. Please set LIBARTNET_ROOT variable")
    endif()
else()
    # Look for locally built libartnet first
    set(LOCAL_LIBARTNET_ROOT "${CMAKE_SOURCE_DIR}/build/external/libartnet")
    
    if(EXISTS "${LOCAL_LIBARTNET_ROOT}/lib/libartnet.a")
        message(STATUS "Found locally built libartnet at ${LOCAL_LIBARTNET_ROOT}")
        add_library(LibArtNet::LibArtNet STATIC IMPORTED)
        set_target_properties(LibArtNet::LibArtNet PROPERTIES
            IMPORTED_LOCATION "${LOCAL_LIBARTNET_ROOT}/lib/libartnet.a"
            INTERFACE_INCLUDE_DIRECTORIES "${LOCAL_LIBARTNET_ROOT}/include"
        )
    else()
        # Fall back to system installation
        find_path(LIBARTNET_INCLUDE_DIR NAMES artnet.h PATHS /usr/include /usr/local/include PATH_SUFFIXES artnet)
        find_library(LIBARTNET_LIBRARY NAMES artnet libartnet PATHS /usr/lib /usr/local/lib)
        
        if(LIBARTNET_INCLUDE_DIR AND LIBARTNET_LIBRARY)
            add_library(LibArtNet::LibArtNet SHARED IMPORTED)
            set_target_properties(LibArtNet::LibArtNet PROPERTIES
                IMPORTED_LOCATION "${LIBARTNET_LIBRARY}"
                INTERFACE_INCLUDE_DIRECTORIES "${LIBARTNET_INCLUDE_DIR}"
            )
        else()
            message(WARNING "libartnet not found. Please install: sudo apt-get install libartnet-dev")
        endif()
    endif()
endif()

# ============================================================================
# Create convenient target for all external dependencies
# ============================================================================
add_library(TCLEDTable_external_deps INTERFACE)

target_link_libraries(TCLEDTable_external_deps INTERFACE
    CLI11::CLI11
    $<$<BOOL:${TCLEDTABLE_BUILD_TESTS}>:unity::framework>
    $<$<BOOL:${TCLEDTABLE_BUILD_PYTHON_BINDINGS}>:pybind11::pybind11>
)

# Platform-specific dependencies
if(WIN32)
    target_link_libraries(TCLEDTable_external_deps INTERFACE
        $<$<TARGET_EXISTS:PahoMqttC::PahoMqttC>:PahoMqttC::PahoMqttC>
        $<$<TARGET_EXISTS:PahoMqttCpp::PahoMqttCpp>:PahoMqttCpp::PahoMqttCpp>
        $<$<TARGET_EXISTS:LibArtNet::LibArtNet>:LibArtNet::LibArtNet>
        ws2_32
    )
else()
    target_link_libraries(TCLEDTable_external_deps INTERFACE
        $<$<TARGET_EXISTS:eclipse-paho-mqtt-c::paho-mqtt3a>:eclipse-paho-mqtt-c::paho-mqtt3a>
        $<$<TARGET_EXISTS:PahoMqttCpp::paho-mqttpp3>:PahoMqttCpp::paho-mqttpp3>
        $<$<TARGET_EXISTS:LibArtNet::LibArtNet>:LibArtNet::LibArtNet>
    )
endif()
