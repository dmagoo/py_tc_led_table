# src/system/service_registry.py
# Whitelist of services for UI control and monitoring

SERVICE_REGISTRY = {
    "manage_effects.service": {
        "label": "Effect Runner",
        "controllable": True
    },
    "monitor-serial.service": {
        "label": "Serial Monitor",
        "controllable": True
    },
    "mosquitto.service": {
        "label": "MQTT Broker",
        "controllable": True
    },
    "eth0-fallback.service": {
        "label": "Ethernet Fallback",
        "controllable": False
    },
    "wlan0-fallback.service": {
        "label": "Wi-Fi Fallback",
        "controllable": False
    }
}
