#ifndef LED_TABLE_CONFIG_H
#define LED_TABLE_CONFIG_H

#include "make_artnet_config.h"

struct LedTableConfig {
    ArtnetConfig artnetConfig;
    bool enableArtnetMessaging;
};

#endif
