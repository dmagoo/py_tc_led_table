#include "LedTableApi.h"
#include "core/node_geometry.h"
#include <iostream>

#include <string>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>

std::string getLocalIPAddress() {
    WSADATA wsaData;
    char hostname[256];
    std::string ip = "";

    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
        return "";

    if (gethostname(hostname, sizeof(hostname)) == SOCKET_ERROR) {
        WSACleanup();
        return "";
    }

    addrinfo hints = {}, *info = nullptr;
    hints.ai_family = AF_INET; // IPv4 only
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_protocol = IPPROTO_TCP;

    if (getaddrinfo(hostname, nullptr, &hints, &info) != 0) {
        WSACleanup();
        return "";
    }

    for (addrinfo* p = info; p != nullptr; p = p->ai_next) {
        sockaddr_in* addr = reinterpret_cast<sockaddr_in*>(p->ai_addr);
        ip = inet_ntoa(addr->sin_addr);
        break; // take the first one
    }

    freeaddrinfo(info);
    WSACleanup();
    return ip;
}
#else
#include <arpa/inet.h>
#include <ifaddrs.h>
#include <netinet/in.h>

std::string getLocalIPAddress() {
    struct ifaddrs *ifaddr, *ifa;
    char ip[INET_ADDRSTRLEN];

    if (getifaddrs(&ifaddr) == -1) return "";

    for (ifa = ifaddr; ifa != nullptr; ifa = ifa->ifa_next) {
        if (!ifa->ifa_addr || ifa->ifa_addr->sa_family != AF_INET) continue;
        void* addr_ptr = &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr;
        inet_ntop(AF_INET, addr_ptr, ip, INET_ADDRSTRLEN);

        std::string name = ifa->ifa_name;
        if (name.find("eth") == 0 || name.find("en") == 0) {
            freeifaddrs(ifaddr);
            return ip;
        }
    }

    freeifaddrs(ifaddr);
    return "";
}
#endif


// Private method to convert WRGB color to the specified format
std::array<uint8_t, 4> LedTableApi::convertColor(WRGB color, ARTNET_PACKET_FORMAT format) {
    // Extract individual components from the WRGB color
    uint8_t w = (color >> 24) & 0xFF;
    uint8_t r = (color >> 16) & 0xFF;
    uint8_t g = (color >> 8) & 0xFF;
    uint8_t b = color & 0xFF;
    
    // Convert to the specified format
    switch (format) {
        case ARTNET_PACKET_FORMAT::WRGB:
            return {w, r, g, b};
        case ARTNET_PACKET_FORMAT::GRBW:
            return {g, r, b, w};
        case ARTNET_PACKET_FORMAT::RGBW:
            return {r, g, b, w};
    }
    // Default to WRGB if format is not recognized
    return {w, r, g, b};
}

template <typename CommandType, typename... Args>
void LedTableApi::performClusterOperationReturningVoid(int nodeId, Args... args) {
    int clusterId = clusterManager.getClusterIdFromNodeId(nodeId);
    const Cluster *clusterPtr = clusterManager.getClusterById(clusterId);
    if (clusterPtr) {
        Cluster &cluster = *const_cast<Cluster *>(clusterPtr); // Cast to non-const reference
        if constexpr (sizeof...(args) >= 2) {
            auto secondArgument = std::get<1>(std::make_tuple(args...));
        }
        //// HERE the seond argument is fine!!  Is the syntax below correct?
        CommandType command(nodeId, args...);
        command.execute(cluster);
    } else {
        // Handle the case where the cluster is not found
    }
}

template <typename CommandType, typename... Args>
WRGB LedTableApi::performClusterOperationReturningColor(int nodeId, Args... args) {
    int clusterId = clusterManager.getClusterIdFromNodeId(nodeId);
    const Cluster *clusterPtr = clusterManager.getClusterById(clusterId);

    if (clusterPtr) {
        Cluster &cluster = *const_cast<Cluster *>(clusterPtr); // Cast to non-const reference
        CommandType command(nodeId, args...);
        return command.execute(cluster);
    } else {
        // Handle the case where the cluster is not found
        return 0;
    }
}

LedTableApi::LedTableApi(ClusterManager &clusterManager, const LedTableConfig &config)
    : clusterManager(clusterManager), suppressMessages(!config.enableArtnetMessaging), artnetClient(nullptr, artnet_deleter) {

    if (config.enableArtnetMessaging) {
      //std::cerr << "has ip!: " << config.artnetConfig.brokerAddress.c_str() << std::endl;
      //initArtnetClient(nullptr); // Replace with actual IP address or config value as needed

      auto ip = getLocalIPAddress();
      initArtnetClient(ip.empty() ? nullptr : ip.c_str());
      // initArtnetClient(config.artnetConfig.brokerAddress.c_str()); // Replace with actual IP address or config value as needed
      int val = artnet_start(artnetClient.get());
        // TODO check for ARTNET_EOK return value
    }
}

// Explicit template instantiations for all the command types you use
template void LedTableApi::performClusterOperationReturningVoid<FillNodeCommand, WRGB>(int, WRGB);
template WRGB LedTableApi::performClusterOperationReturningColor<QueueNodePixelCommand, WRGB>(int, WRGB);
template WRGB LedTableApi::performClusterOperationReturningColor<DequeueNodePixelCommand>(int, WRGB);

// Template specialization for RingCoordinate
template <>
int LedTableApi::convertToNodeId<RingCoordinate>(const RingCoordinate &coordinate) {
    return clusterManager.getNodeId(coordinate);
}

// Template specialization for Cartesian2dCoordinate
template <>
int LedTableApi::convertToNodeId<Cartesian2dCoordinate>(const Cartesian2dCoordinate &coordinate) {
    return clusterManager.getNodeId(coordinate);
}

// Template specialization for CubeCoordinate
template <>
int LedTableApi::convertToNodeId<CubeCoordinate>(const CubeCoordinate &coordinate) {
    return clusterManager.getNodeId(coordinate);
}

void LedTableApi::fillNode(int nodeId, WRGB color) {
    performClusterOperationReturningVoid<FillNodeCommand>(nodeId, color);
}

void LedTableApi::fillNode(RingCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<FillNodeCommand>(nodeId, color);
}

void LedTableApi::fillNode(CubeCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<FillNodeCommand>(nodeId, color);
}

void LedTableApi::fillNode(Cartesian2dCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<FillNodeCommand>(nodeId, color);
}

void LedTableApi::fillNode(int nodeId, const std::vector<WRGB> &colors, WRGB padColor) {
    performClusterOperationReturningVoid<BlitNodeCommand>(nodeId, colors, padColor);
}

void LedTableApi::fillNode(RingCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padColor) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<BlitNodeCommand>(nodeId, colors, padColor);
}

void LedTableApi::fillNode(CubeCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padColor) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<BlitNodeCommand>(nodeId, colors, padColor);
}

void LedTableApi::fillNode(Cartesian2dCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padColor) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<BlitNodeCommand>(nodeId, colors, padColor);
}

// Implementations of the public API methods using the template function
void LedTableApi::setNodePixel(int nodeId, int pixelIndex, WRGB color) {
    performClusterOperationReturningVoid<SetNodePixelCommand>(nodeId, pixelIndex, color);
}

void LedTableApi::setNodePixel(RingCoordinate coordinate, int pixelIndex, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<SetNodePixelCommand>(nodeId, pixelIndex, color);
}

void LedTableApi::setNodePixel(CubeCoordinate coordinate, int pixelIndex, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<SetNodePixelCommand>(nodeId, pixelIndex, color);
}

void LedTableApi::setNodePixel(Cartesian2dCoordinate coordinate, int pixelIndex, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    performClusterOperationReturningVoid<SetNodePixelCommand>(nodeId, pixelIndex, color);
}

// Implementations of the public API methods using the template function
WRGB LedTableApi::queueNodePixel(int nodeId, WRGB color) {
    return performClusterOperationReturningColor<QueueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::queueNodePixel(RingCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<QueueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::queueNodePixel(CubeCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<QueueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::queueNodePixel(Cartesian2dCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<QueueNodePixelCommand>(nodeId, color);
}

// Implementations of the public API methods using the template function
WRGB LedTableApi::dequeueNodePixel(int nodeId, WRGB color) {
    return performClusterOperationReturningColor<DequeueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::dequeueNodePixel(RingCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<DequeueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::dequeueNodePixel(CubeCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<DequeueNodePixelCommand>(nodeId, color);
}

WRGB LedTableApi::dequeueNodePixel(Cartesian2dCoordinate coordinate, WRGB color) {
    int nodeId = convertToNodeId(coordinate);
    return performClusterOperationReturningColor<DequeueNodePixelCommand>(nodeId, color);
}

std::vector<int> LedTableApi::listNodeIds() {
    return clusterManager.listNodeIds();
}

int LedTableApi::getNodeId(const RingCoordinate &coords) const {
    return clusterManager.getNodeId(coords);
}
int LedTableApi::getNodeId(const CubeCoordinate &coords) const {
    return clusterManager.getNodeId(coords);
}
int LedTableApi::getNodeId(const Cartesian2dCoordinate &coords) const {
    return clusterManager.getNodeId(coords);
}

RingCoordinate LedTableApi::getRingCoordinate(int nodeId) const {
    return clusterManager.getRingCoordinate(nodeId);
}
CubeCoordinate LedTableApi::getCubeCoordinate(int nodeId) const {
    return clusterManager.getCubeCoordinate(nodeId);
}
Cartesian2dCoordinate LedTableApi::getCartesian2dCoordinate(int nodeId) const {
    return clusterManager.getCartesian2dCoordinate(nodeId);
}

std::vector<WRGB> LedTableApi::getNodePixelBuffer(int nodeId) {
    int clusterId = clusterManager.getClusterIdFromNodeId(nodeId);
    const Cluster *clusterPtr = clusterManager.getClusterById(clusterId);
    return clusterPtr->getNodePixelBuffer(nodeId);
}
std::vector<WRGB> LedTableApi::getNodePixelBuffer(RingCoordinate coordinate) {
    int nodeId = convertToNodeId(coordinate);
    return getNodePixelBuffer(nodeId);
}
std::vector<WRGB> LedTableApi::getNodePixelBuffer(Cartesian2dCoordinate coordinate) {
    int nodeId = convertToNodeId(coordinate);
    return getNodePixelBuffer(nodeId);
}
std::vector<WRGB> LedTableApi::getNodePixelBuffer(CubeCoordinate coordinate) {
    int nodeId = convertToNodeId(coordinate);
    return getNodePixelBuffer(nodeId);
}

std::vector<int> LedTableApi::getNodePath(int nodeIdA, int nodeIdB) {
    std::vector<int> values = node_geometry::get_node_path(nodeIdA, nodeIdB, clusterManager);
    return values;
}
std::vector<int> LedTableApi::getNodePath(RingCoordinate coordinateA, RingCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return {};
}
std::vector<int> LedTableApi::getNodePath(Cartesian2dCoordinate coordinateA, Cartesian2dCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return {};
}
std::vector<int> LedTableApi::getNodePath(CubeCoordinate coordinateA, CubeCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return {};
}

std::vector<int> LedTableApi::getNodeNeighbors(int nodeId, int level) {
    return node_geometry::get_node_neighbors(nodeId, clusterManager, level);
}
std::vector<int> LedTableApi::getNodeNeighbors(RingCoordinate coordinate, int level) {
    int nodeId = convertToNodeId(coordinate);
    return getNodeNeighbors(nodeId, level);
}
std::vector<int> LedTableApi::getNodeNeighbors(Cartesian2dCoordinate coordinate, int level) {
    int nodeId = convertToNodeId(coordinate);
    return getNodeNeighbors(nodeId, level);
}
std::vector<int> LedTableApi::getNodeNeighbors(CubeCoordinate coordinate, int level) {
    int nodeId = convertToNodeId(coordinate);
    return getNodeNeighbors(nodeId, level);
}

std::tuple<int, int> LedTableApi::getFacingPixelIndexes(int nodeIdA, int nodeIdB) {
    return node_geometry::get_facing_pixel_indexes(nodeIdA, nodeIdB, clusterManager);
}
std::tuple<int, int> LedTableApi::getFacingPixelIndexes(RingCoordinate coordinateA, RingCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return getFacingPixelIndexes(nodeIdA, nodeIdB);
}
std::tuple<int, int> LedTableApi::getFacingPixelIndexes(Cartesian2dCoordinate coordinateA, Cartesian2dCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return getFacingPixelIndexes(nodeIdA, nodeIdB);
}
std::tuple<int, int> LedTableApi::getFacingPixelIndexes(CubeCoordinate coordinateA, CubeCoordinate coordinateB) {
    int nodeIdA = convertToNodeId(coordinateA);
    int nodeIdB = convertToNodeId(coordinateB);
    return getFacingPixelIndexes(nodeIdA, nodeIdB);
}

void LedTableApi::setSuppressMessages(bool newValue) {
    suppressMessages = newValue;
}

// ignores suppressMessges, as this is an explicit command to send a message
void LedTableApi::refresh() {
    clusterManager.forEachCluster([this](Cluster &cluster) { // Capture `this` to access class members
        this->sendClusterArtnet(cluster.getId(), cluster.getPixelBuffer());
    });
}

void LedTableApi::reset() {
    clusterManager.forEachCluster([this](Cluster &cluster) {
        FillBufferCommand command(0x00000000);
        command.execute(cluster);
        if (!suppressMessages) {
          this->sendClusterArtnet(cluster.getId(), cluster.getPixelBuffer());
        }
    });
}

void LedTableApi::initArtnetClient(const char *ip) {
    artnet_node raw_ptr = artnet_new(ip, 0); // 0 is a "verbose" flag
    if (raw_ptr != nullptr) {
        artnetClient.reset(raw_ptr);
        clusterManager.forEachCluster([this](Cluster &cluster) {
            if (artnet_set_port_addr(this->artnetClient.get(), cluster.getId(), ARTNET_INPUT_PORT, cluster.getId()) != ARTNET_EOK) {
                // Handle error
                std::cerr << "failed to map artnet port" << std::endl;
            }
        });
        artnet_dump_config(artnetClient.get());
    } else {
        std::cerr << "Error" << artnet_strerror() << std::endl;
        // Handle the case where artnet_new fails
        // For example, log an error or throw an exception
    }
}

void LedTableApi::sendClusterArtnet(int clusterId, const std::vector<WRGB> buffer) {
    if (artnetClient) {
        std::vector<uint8_t> dmxData;
        dmxData.reserve(buffer.size() * 4); // Assuming WRGB to RGB conversion
        for (WRGB color : buffer) {
            //    dmxData.push_back((color >> 24) & 0xFF); // White
            //    dmxData.push_back((color >> 16) & 0xFF); // Red
            //    dmxData.push_back((color >> 8) & 0xFF);  // Green
            //    dmxData.push_back(color & 0xFF);         // Blue
            std::array<uint8_t, 4> convertedColor = convertColor(color, ARTNET_PACKET_FORMAT::GRBW);
            // Append the converted color to the DMX data
            dmxData.insert(dmxData.end(), convertedColor.begin(), convertedColor.end());

        }
        if (artnet_send_dmx(artnetClient.get(), clusterId, dmxData.size(), dmxData.data()) != ARTNET_EOK) {
            std::cerr << "Error" << artnet_strerror() << std::endl;
        }
    } else {
        std::cerr << "NO ART NET" << std::endl;
    }
}



