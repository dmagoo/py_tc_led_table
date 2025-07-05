cmake_minimum_required(VERSION 3.16)

# Project configuration
project(TCLEDTable 
    VERSION 1.0.0
    LANGUAGES CXX
    DESCRIPTION "LED Table Control System with Python Bindings"
)

# Set policies for better CMake behavior
cmake_policy(SET CMP0077 NEW)  # option() honors normal variables
cmake_policy(SET CMP0083 NEW)  # Honor visibility properties

# Project-wide settings
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Include custom CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/Modules")

# Include configuration files
include(cmake/CompilerSettings.cmake)
include(cmake/Dependencies.cmake)

# Build options
option(TCLEDTABLE_BUILD_TESTS "Build unit tests" ${PROJECT_IS_TOP_LEVEL})
option(TCLEDTABLE_BUILD_PYTHON_BINDINGS "Build Python bindings" ON)
option(TCLEDTABLE_BUILD_EXAMPLES "Build examples" ${PROJECT_IS_TOP_LEVEL})
option(TCLEDTABLE_INSTALL "Generate install target" ${PROJECT_IS_TOP_LEVEL})

# Enable testing if requested
if(TCLEDTABLE_BUILD_TESTS)
    enable_testing()
    include(CTest)
endif()

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Main library
add_subdirectory(src)

# Python bindings
if(TCLEDTABLE_BUILD_PYTHON_BINDINGS)
    add_subdirectory(bindings)
endif()

# Tests
if(TCLEDTABLE_BUILD_TESTS)
    add_subdirectory(tests)
endif()

# Examples
if(TCLEDTABLE_BUILD_EXAMPLES)
    # Examples would go here
endif()

# Installation
if(TCLEDTABLE_INSTALL)
    include(GNUInstallDirs)
    include(cmake/Install.cmake)
endif()

# Export targets
if(TCLEDTABLE_INSTALL)
    export(EXPORT TCLEDTableTargets
        FILE "${CMAKE_CURRENT_BINARY_DIR}/TCLEDTableTargets.cmake"
        NAMESPACE TCLEDTable::
    )
endif()
