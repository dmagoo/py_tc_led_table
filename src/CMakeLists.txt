# CMakeLists.txt for the main TC LED Table library

# Create the main library target
add_library(TCLEDTableCore
    tc_led_table/core/Cluster.cpp
    tc_led_table/core/ClusterConfig.cpp
    tc_led_table/core/ClusterManager.cpp
    tc_led_table/core/Node.cpp
    tc_led_table/core/NodeConfig.cpp
    tc_led_table/core/node_geometry.cpp
    tc_led_table/core/coordinates/Cartesian2dCoordinate.cpp
    tc_led_table/core/coordinates/CubeCoordinate.cpp
    tc_led_table/core/coordinates/RingCoordinate.cpp
    tc_led_table/config/led_table_config.cpp
    tc_led_table/config/make_cluster_config.cpp
    tc_led_table/config/make_artnet_config.cpp
    tc_led_table/api/LedTableApi.cpp
)

# Add platform-specific sources
if(WIN32)
    target_sources(TCLEDTableCore PRIVATE
        tc_led_table/platform/windows/AsciiUtils.cpp
    )
endif()

# Set target properties
set_target_properties(TCLEDTableCore PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    POSITION_INDEPENDENT_CODE ON
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
)

# Include directories
target_include_directories(TCLEDTableCore
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/tc_led_table
)

# Link dependencies
target_link_libraries(TCLEDTableCore
    PUBLIC
        TCLEDTable_external_deps
        TCLEDTable_warnings
    PRIVATE
        # Platform-specific libraries
        $<$<PLATFORM_ID:Windows>:LibArtNet::LibArtNet>
        $<$<NOT:$<PLATFORM_ID:Windows>>:LibArtNet::LibArtNet>
)

# Create alias for consistent naming
add_library(TCLEDTable::Core ALIAS TCLEDTableCore)

# Add subdirectories for additional components
if(TCLEDTABLE_BUILD_TESTS)
    # Tests would be added here if we had src-level tests
endif()

# Export targets
if(TCLEDTABLE_INSTALL)
    install(TARGETS TCLEDTableCore
        EXPORT TCLEDTableTargets
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    )
endif()
