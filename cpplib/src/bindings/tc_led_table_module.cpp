#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "LedTableApi.h"
#include "config/led_table_config.h"
#include "config/make_cluster_config.h"
#include "core/ClusterManager.h"

namespace py = pybind11;

// Assuming these functions are defined in their respective .cpp files
void init_coordinate_bindings(py::module_ &);
void init_led_table_config_bindings(py::module_ &);

std::shared_ptr<LedTableApi> init(LedTableConfig *config = nullptr) {
  static std::shared_ptr<LedTableApi> apiSharedPtr;

  if(apiSharedPtr) {
    return apiSharedPtr;
      }


  static ClusterManager clusterManager(makeClusterConfigs());
  std::cout << "SET UP CONF" << std::endl;

  LedTableConfig effectiveConfig;
  effectiveConfig.artnetConfig.brokerAddress = "192.168.1.50";
  // effectiveConfig.artnetConfig.brokerAddress = "tcp://localhost";  
  //  effectiveConfig.artnetConfig.brokerAddress = "127.0.0.1";

  if (config != nullptr) {
    //std::cout << "SET UP CONF2" << std::endl;
    //effectiveConfig = *config;
    //effectiveConfig.artnetConfig.brokerAddress = "192.168.1.50";
  } else {
    effectiveConfig.artnetConfig.brokerAddress = "192.168.1.50";
  }

  apiSharedPtr = std::make_shared<LedTableApi>(clusterManager, effectiveConfig);


  return apiSharedPtr;
}

void bootstrap(LedTableConfig *config = nullptr) {
  //std::cout << "BOOTSTRAP" << std::endl;
  init(config);
}

PYBIND11_MODULE(tc_led_table, m) {
    init_coordinate_bindings(m);
    init_led_table_config_bindings(m);

    m.def("init", &bootstrap, py::arg("config") = nullptr, "Function to initialize and get the API instance with an optional configuration");
    m.def(
        "setSuppressMessages", [](bool suppress) {
            auto api = init();
            api->setSuppressMessages(suppress);
        },
        "A function to set suppress messages");

    // fillNode methods
    m.def("fillNode", [](int nodeId, const WRGB &color) {
        auto api = init();
        api->fillNode(nodeId, color);
    });
    m.def("fillNode", [](const RingCoordinate &coordinate, const WRGB &color) {
        auto api = init();
        api->fillNode(coordinate, color);
    });
    m.def("fillNode", [](const Cartesian2dCoordinate &coordinate, const WRGB &color) {
        auto api = init();
        api->fillNode(coordinate, color);
    });
    m.def("fillNode", [](const CubeCoordinate &coordinate, const WRGB &color) {
        auto api = init();
        api->fillNode(coordinate, color);
    });

    // Overloaded fillNode methods with color arrays and pad color
    m.def("fillNode", [](int nodeId, const std::vector<WRGB> &colors, WRGB padcolor) {
        auto api = init();
        api->fillNode(nodeId, colors, padcolor);
    });
    m.def("fillNode", [](const RingCoordinate &coordinate, const std::vector<WRGB> &colors, WRGB padcolor) {
        auto api = init();
        api->fillNode(coordinate, colors, padcolor);
    });
    m.def("fillNode", [](const Cartesian2dCoordinate &coordinate, const std::vector<WRGB> &colors, WRGB padcolor) {
        auto api = init();
        api->fillNode(coordinate, colors, padcolor);
    });
    m.def("fillNode", [](const CubeCoordinate &coordinate, const std::vector<WRGB> &colors, WRGB padcolor) {
        auto api = init();
        api->fillNode(coordinate, colors, padcolor);
    });

    // setNodePixel methods
    m.def("setNodePixel", [](int nodeId, int pixelIndex, WRGB color) {
        auto api = init();
        api->setNodePixel(nodeId, pixelIndex, color);
    });
    m.def("setNodePixel", [](const RingCoordinate &coordinate, int pixelIndex, WRGB color) {
        auto api = init();
        api->setNodePixel(coordinate, pixelIndex, color);
    });
    m.def("setNodePixel", [](const Cartesian2dCoordinate &coordinate, int pixelIndex, WRGB color) {
        auto api = init();
        api->setNodePixel(coordinate, pixelIndex, color);
    });
    m.def("setNodePixel", [](const CubeCoordinate &coordinate, int pixelIndex, WRGB color) {
        auto api = init();
        api->setNodePixel(coordinate, pixelIndex, color);
    });

    // queueNodePixel methods
    m.def("queueNodePixel", [](int nodeId, WRGB color) -> WRGB {
        auto api = init();
        return api->queueNodePixel(nodeId, color);
    });
    m.def("queueNodePixel", [](const RingCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->queueNodePixel(coordinate, color);
    });
    m.def("queueNodePixel", [](const Cartesian2dCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->queueNodePixel(coordinate, color);
    });
    m.def("queueNodePixel", [](const CubeCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->queueNodePixel(coordinate, color);
    });

    // dequeueNodePixel methods
    m.def("dequeueNodePixel", [](int nodeId, WRGB color) -> WRGB {
        auto api = init();
        return api->dequeueNodePixel(nodeId, color);
    });
    m.def("dequeueNodePixel", [](const RingCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->dequeueNodePixel(coordinate, color);
    });
    m.def("dequeueNodePixel", [](const Cartesian2dCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->dequeueNodePixel(coordinate, color);
    });
    m.def("dequeueNodePixel", [](const CubeCoordinate &coordinate, WRGB color) -> WRGB {
        auto api = init();
        return api->dequeueNodePixel(coordinate, color);
    });

    m.def("listNodeIds", []() -> std::vector<int> {
        auto api = init();
        return api->listNodeIds();
    });

    m.def("getNodeId", [](const RingCoordinate &coordinate) -> int {
        auto api = init();
        return api->getNodeId(coordinate);
    });

    m.def("getNodeId", [](const Cartesian2dCoordinate &coordinate) -> int {
        auto api = init();
        return api->getNodeId(coordinate);
    });

    m.def("getNodeId", [](const CubeCoordinate &coordinate) -> int {
        auto api = init();
        return api->getNodeId(coordinate);
    });

    m.def("getRingCoordinate", [](int nodeId) -> RingCoordinate {
        auto api = init();
        return api->getRingCoordinate(nodeId);
    });
    m.def("getCartesian2dCoordinate", [](int nodeId) -> Cartesian2dCoordinate {
        auto api = init();
        return api->getCartesian2dCoordinate(nodeId);
    });
    m.def("getCubeCoordinate", [](int nodeId) -> CubeCoordinate {
        auto api = init();
        return api->getCubeCoordinate(nodeId);
    });

    // getNodePixelBuffer methods
    m.def("getNodePixelBuffer", [](int nodeId) -> std::vector<WRGB> {
        auto api = init();
        return api->getNodePixelBuffer(nodeId);
    });
    m.def("getNodePixelBuffer", [](const RingCoordinate &coordinate) -> std::vector<WRGB> {
        auto api = init();
        return api->getNodePixelBuffer(coordinate);
    });
    m.def("getNodePixelBuffer", [](const Cartesian2dCoordinate &coordinate) -> std::vector<WRGB> {
        auto api = init();
        return api->getNodePixelBuffer(coordinate);
    });
    m.def("getNodePixelBuffer", [](const CubeCoordinate &coordinate) -> std::vector<WRGB> {
        auto api = init();
        return api->getNodePixelBuffer(coordinate);
    });

    // getNodePath methods
    m.def("getNodePath", [](int nodeIdA, int nodeIdB) -> std::vector<int> {
        auto api = init();
        return api->getNodePath(nodeIdA, nodeIdB);
    });
    m.def("getNodePath", [](const RingCoordinate &coordinateA, const RingCoordinate &coordinateB) -> std::vector<int> {
        auto api = init();
        return api->getNodePath(coordinateA, coordinateB);
    });
    m.def("getNodePath", [](const Cartesian2dCoordinate &coordinateA, const Cartesian2dCoordinate &coordinateB) -> std::vector<int> {
        auto api = init();
        return api->getNodePath(coordinateA, coordinateB);
    });
    m.def("getNodePath", [](const CubeCoordinate &coordinateA, const CubeCoordinate &coordinateB) -> std::vector<int> {
        auto api = init();
        return api->getNodePath(coordinateA, coordinateB);
    });

    // getNodeNeighbors methods
    m.def("getNodeNeighbors", [](int nodeId, int level) -> std::vector<int> {
        auto api = init();
        return api->getNodeNeighbors(nodeId, level);
    });
    m.def("getNodeNeighbors", [](const RingCoordinate &coordinate, int level) -> std::vector<int> {
        auto api = init();
        return api->getNodeNeighbors(coordinate, level);
    });
    m.def("getNodeNeighbors", [](const Cartesian2dCoordinate &coordinate, int level) -> std::vector<int> {
        auto api = init();
        return api->getNodeNeighbors(coordinate, level);
    });
    m.def("getNodeNeighbors", [](const CubeCoordinate &coordinate, int level) -> std::vector<int> {
        auto api = init();
        return api->getNodeNeighbors(coordinate, level);
    });

    // getFacingPixelIndexes methods
    m.def("getFacingPixelIndexes", [](int nodeIdA, int nodeIdB) -> std::tuple<int, int> {
        auto api = init();
        return api->getFacingPixelIndexes(nodeIdA, nodeIdB);
    });
    m.def("getFacingPixelIndexes", [](const RingCoordinate &coordinateA, const RingCoordinate &coordinateB) -> std::tuple<int, int> {
        auto api = init();
        return api->getFacingPixelIndexes(coordinateA, coordinateB);
    });
    m.def("getFacingPixelIndexes", [](const Cartesian2dCoordinate &coordinateA, const Cartesian2dCoordinate &coordinateB) -> std::tuple<int, int> {
        auto api = init();
        return api->getFacingPixelIndexes(coordinateA, coordinateB);
    });
    m.def("getFacingPixelIndexes", [](const CubeCoordinate &coordinateA, const CubeCoordinate &coordinateB) -> std::tuple<int, int> {
        auto api = init();
        return api->getFacingPixelIndexes(coordinateA, coordinateB);
    });


    m.def("reset", []() {
        auto api = init();
        api->reset();
    });
    m.def("refresh", []() {
        auto api = init();
        api->refresh();
    });
}
