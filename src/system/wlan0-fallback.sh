#!/bin/bash
# Wi-Fi fallback for LED Table Pi
# Triggers hotspot mode if wlan0 does not receive a real IP via DHCP/wpa_supplicant
# Copy to: /usr/local/bin/wlan0-fallback.sh

sleep 20  # Give DHCP/wpa_supplicant enough time

IFACE="wlan0"

# Force DHCP
sudo dhclient "$IFACE"

# Check for any valid IP except fallback
CONNECTED=$(ip addr show "$IFACE" | grep "inet " | grep -v "192.168.4")

if [ -n "$CONNECTED" ]; then
    echo "Wi-Fi is connected. Hotspot not needed."
    exit 0
fi

echo "No Wi-Fi connection. Enabling hotspot mode."

ip link set "$IFACE" down
ip addr flush dev "$IFACE"
ip addr add 192.168.4.1/24 dev "$IFACE"
ip link set "$IFACE" up

systemctl restart hostapd
systemctl restart dnsmasq
