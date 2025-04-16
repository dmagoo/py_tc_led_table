#!/bin/bash
# /usr/local/bin/wlan0-fallback.sh
# Copy to: /usr/local/bin/
# Enables Wi-Fi hotspot if Pi is not connected to a Wi-Fi network
# Paired with: /etc/systemd/system/wlan0-fallback.service

sleep 10

# Check for IP assigned to wlan0 by DHCP (indicating successful Wi-Fi connection)
ip addr show wlan0 | grep "inet 192.168" > /dev/null
if [ $? -ne 0 ]; then
    echo "No Wi-Fi connection. Enabling hotspot mode."

    # Assign static IP
    ip addr flush dev wlan0
    ip addr add 192.168.4.1/24 dev wlan0
    ip link set wlan0 up

    # Start services
    systemctl start dnsmasq
    systemctl start hostapd
else
    echo "Wi-Fi is connected. Hotspot not needed."
fi
