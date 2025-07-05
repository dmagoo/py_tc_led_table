# Installation configuration for TCLEDTable

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

# Create package config files
configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/TCLEDTableConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/TCLEDTableConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TCLEDTable
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/TCLEDTableConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY AnyNewerVersion
)

# Install targets
install(EXPORT TCLEDTableTargets
    FILE TCLEDTableTargets.cmake
    NAMESPACE TCLEDTable::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TCLEDTable
)

# Install config files
install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/TCLEDTableConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/TCLEDTableConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/TCLEDTable
)

# Install headers
install(DIRECTORY src/tc_led_table/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/tc_led_table
    FILES_MATCHING PATTERN "*.h" PATTERN "*.hpp"
)

# Install documentation
if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/docs")
    install(DIRECTORY docs/
        DESTINATION ${CMAKE_INSTALL_DOCDIR}
        OPTIONAL
    )
endif()

# Install examples
if(TCLEDTABLE_BUILD_EXAMPLES AND EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/examples")
    install(DIRECTORY examples/
        DESTINATION ${CMAKE_INSTALL_DOCDIR}/examples
        OPTIONAL
    )
endif()

# Create uninstall target
if(NOT TARGET uninstall)
    configure_file(
        "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
        "${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake"
        IMMEDIATE @ONLY
    )

    add_custom_target(uninstall
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
    )
endif()
