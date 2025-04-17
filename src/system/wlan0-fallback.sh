#!/bin/bash
# Wi-Fi fallback for LED Table Pi
# Triggers if wlan0 does not get a valid IP from wpa_supplicant
# Starts hotspot mode with static IP 192.168.4.1

sleep 10

IFACE="wlan0"

# Ignore fallback IP (192.168.4.x) if already set
CONNECTED=$(ip addr show $IFACE | grep "inet " | grep -v "192.168.4")

if [ -n "$CONNECTED" ]; then
    echo "Wi-Fi is connected. Hotspot not needed."
    exit 0
fi

echo "No Wi-Fi connection. Enabling hotspot mode."

ip link set $IFACE down
ip addr flush dev $IFACE
ip addr add 192.168.4.1/24 dev $IFACE
ip link set $IFACE up

systemctl restart hostapd
systemctl restart dnsmasq
