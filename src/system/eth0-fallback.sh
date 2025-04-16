#!/bin/bash

# Copy to: /usr/local/bin/eth0-fallback.sh

# Wait for DHCP to do its thing
sleep 10

# Check if eth0 has an IP from DHCP
ip addr show eth0 | grep "inet 192.168.1" > /dev/null
if [ $? -ne 0 ]; then
    echo "No DHCP lease on eth0. Enabling fallback static IP and dnsmasq."

    # Set static IP
    ip addr flush dev eth0
    ip addr add 192.168.1.10/24 dev eth0
    ip link set eth0 up

    # Start dnsmasq manually
    systemctl start dnsmasq
else
    echo "DHCP lease on eth0 found. No action taken."
fi
