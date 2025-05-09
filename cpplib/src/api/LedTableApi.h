#ifndef LEDTABLEAPI_H
#define LEDTABLEAPI_H

#include "config/led_table_config.h"
#include "core/ClusterCommands.h"
#include "core/ClusterManager.h"
#include "core/coordinates/Cartesian2dCoordinate.h"
#include "core/coordinates/CubeCoordinate.h"
#include "core/coordinates/RingCoordinate.h"

#include <artnet.h>

// Define enum for color formats
enum class ARTNET_PACKET_FORMAT {
    RGBW,
    WRGB,
    GRBW
};

static void artnet_deleter(void *ptr) {
    if (ptr) {
        artnet_destroy(ptr); // Assuming artnet_destroy is compatible with void* argument
    }
}

class LedTableApi {

private:
    ClusterManager &clusterManager;
    std::unique_ptr<void, void (*)(void *)> artnetClient;

    bool suppressMessages = false;

    std::array<uint8_t, 4> convertColor(WRGB color, ARTNET_PACKET_FORMAT format);

    template <typename CoordinateType>
    int convertToNodeId(const CoordinateType &coordinate);

    template <typename CommandType, typename... Args>
    void performClusterOperationReturningVoid(int nodeId, Args... args);

    template <typename CommandType, typename... Args>
    WRGB performClusterOperationReturningColor(int nodeId, Args... args);

    void sendClusterArtnet(int clusterId, const std::vector<WRGB> buffer);
    void initArtnetClient(const char *ip);

public:
    explicit LedTableApi(ClusterManager &clusterManager, const LedTableConfig &config = LedTableConfig());

    void setSuppressMessages(bool newValue);

    void fillNode(int nodeId, WRGB color);
    void fillNode(RingCoordinate coordinate, WRGB color);
    void fillNode(Cartesian2dCoordinate coordinate, WRGB color);
    void fillNode(CubeCoordinate coordinate, WRGB color);

    void fillNode(int nodeId, const std::vector<WRGB> &colors, WRGB padcolor);
    void fillNode(RingCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padcolor);
    void fillNode(Cartesian2dCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padcolor);
    void fillNode(CubeCoordinate coordinate, const std::vector<WRGB> &colors, WRGB padcolor);

    void setNodePixel(int nodeId, int pixelIndex, WRGB color);
    void setNodePixel(RingCoordinate coordinate, int pixelIndex, WRGB color);
    void setNodePixel(Cartesian2dCoordinate coordinate, int pixelIndex, WRGB color);
    void setNodePixel(CubeCoordinate coordinate, int pixelIndex, WRGB color);

    WRGB queueNodePixel(int nodeId, WRGB color);
    WRGB queueNodePixel(RingCoordinate coordinate, WRGB color);
    WRGB queueNodePixel(Cartesian2dCoordinate coordinate, WRGB color);
    WRGB queueNodePixel(CubeCoordinate coordinate, WRGB color);

    WRGB dequeueNodePixel(int nodeId, WRGB color);
    WRGB dequeueNodePixel(RingCoordinate coordinate, WRGB color);
    WRGB dequeueNodePixel(Cartesian2dCoordinate coordinate, WRGB color);
    WRGB dequeueNodePixel(CubeCoordinate coordinate, WRGB color);

    std::vector<int> listNodeIds();

    int getNodeId(const RingCoordinate &coords) const;
    int getNodeId(const CubeCoordinate &coords) const;
    int getNodeId(const Cartesian2dCoordinate &coords) const;

    RingCoordinate getRingCoordinate(int nodeId) const;
    CubeCoordinate getCubeCoordinate(int nodeId) const;
    Cartesian2dCoordinate getCartesian2dCoordinate(int nodeId) const;

    // return the pixel buffer for a single node
    std::vector<WRGB> getNodePixelBuffer(int nodeId);
    std::vector<WRGB> getNodePixelBuffer(RingCoordinate coordinate);
    std::vector<WRGB> getNodePixelBuffer(Cartesian2dCoordinate coordinate);
    std::vector<WRGB> getNodePixelBuffer(CubeCoordinate coordinate);

    std::vector<int> getNodePath(int nodeIdA, int nodeIdB);
    std::vector<int> getNodePath(RingCoordinate coordinateA, RingCoordinate coordinateB);
    std::vector<int> getNodePath(Cartesian2dCoordinate coordinateA, Cartesian2dCoordinate coordinateB);
    std::vector<int> getNodePath(CubeCoordinate coordinateA, CubeCoordinate coordinateB);

    std::vector<int> getNodeNeighbors(int nodeId, int level = 1);
    std::vector<int> getNodeNeighbors(RingCoordinate coordinate, int level = 1);
    std::vector<int> getNodeNeighbors(Cartesian2dCoordinate coordinate, int level = 1);
    std::vector<int> getNodeNeighbors(CubeCoordinate coordinate, int level = 1);

    std::tuple<int, int> getFacingPixelIndexes(int nodeIdA, int nodeIdB);
    std::tuple<int, int> getFacingPixelIndexes(RingCoordinate coordinateA, RingCoordinate coordinateB);
    std::tuple<int, int> getFacingPixelIndexes(Cartesian2dCoordinate coordinateA, Cartesian2dCoordinate coordinateB);
    std::tuple<int, int> getFacingPixelIndexes(CubeCoordinate coordinateA, CubeCoordinate coordinateB);


    // contacts all clusters, asking them to fill their buffers black, could any color fill?
    void reset();

    // sends state to all clusters via simple fillbuffer commands
    // using the local models buffer
    // effectively updating / syncing the models. Useful if messages is off
    void refresh();

    // more ideas!
    // copyNode(nodeIdA, nodeIdB) // copies the buffer from a to b, using padding if not equaly sized
};

#endif // LEDTABLEAPI_H
