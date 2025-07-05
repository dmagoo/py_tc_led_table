add_library(CoreLib
    Cluster.cpp
    ClusterConfig.cpp
    ClusterManager.cpp
    Node.cpp
    NodeConfig.cpp
    node_geometry.cpp
    coordinates/Cartesian2dCoordinate.cpp
    coordinates/CubeCoordinate.cpp
    coordinates/RingCoordinate.cpp
    )
set_target_properties(CoreLib PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(CoreLib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
