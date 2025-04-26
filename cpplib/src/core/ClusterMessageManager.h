// ClusterMessageManager.h
#ifndef CLUSTERMESSAGEMANAGER_H
#define CLUSTERMESSAGEMANAGER_H
#include "ClusterCommands.h"
#include "ClusterMessage.h"
#include "config/led_table_config.h"
#include <sstream>

#include <memory>

class ClusterMessageManager {
    // using CommandCallback = std::function<void(int clusterId, ClusterCommandType commandType, std::any params)>;

private:
    int lastSequenceNumber = 0;
    bool connected = false;

public:
    explicit ClusterMessageManager(const LedTableConfig &config);

    template <typename CommandType>
    void sendClusterCommand(int clusterId, const CommandType &command);
};

template <typename CommandType>
void ClusterMessageManager::sendClusterCommand(int clusterId, const CommandType &command) {
    ClusterMessage clusterMessage(clusterId, command.getType(), command.getParams());
}

#endif // CLUSTERMESSAGEMANAGER_H
