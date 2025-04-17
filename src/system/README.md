# LED Table Raspberry Pi System Setup

This document describes the current system configuration for the Raspberry Pi used in the LED Table project. This includes final setups, scripts, and safety-net behavior fallbacks.

## Interface Behavior

The Pi supports two interfaces with forward-fallback modes:

- **Ethernet (eth0)**:
  - Default is DHCP via router or connected scheme.
  - If no IP is received, it sets a static IP to: `192.168.1.10`.
  - Serves DHCP from the Pi to the LED Art-Net controller when no other infrastructure is available.

- **Wi-Fi (wlan0)**:
  - Checks with `wpa_supplicant` for known networks using `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`.
  - If none are available, it sets a static IP: `192.168.4.1`.
  - Restarts `hostapd` and `dnsmasq` for hotspot mode.

## Scripts and Services

The system relies on simple, enabled systemd services to ensure fallback coverage without relying on NetworkManager.

### Ethernet Fallback

- Script: `/src/system/eth0-fallback.sh`
- Static IP: `192.168.1.10/24`
- Dnsmasq Config: `/etc/dnsmasq.d/eth0.conf`
- Service: `/src/system/eth0-fallback.service`

```sh
sudo chmod +x /usr/local/bin/eth0-fallback.sh
sudo systemctl enable eth0-fallback.service
```

### Wi-Fi Fallback

- Script: `/src/system/wlan0-fallback.sh`
- Static IP: `192.168.4.1/24`
- Config Files:
  - `/etc/hostapd/hostapd.conf`
  - `/etc/dnsmasq.d/wlan0.conf`
  - `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`
- Service: `/src/system/wlan0-fallback.service`

```sh
sudo chmod +x /usr/local/bin/wlan0-fallback.sh
sudo systemctl enable wlan0-fallback.service
```

Sample fallback script logic:
```sh
connected=$(ip addr show wlan0 | grep "inet " | grep -v "192.168.4")
if [ -n "$connected" ]; then
    echo "Wi-Fi is connected. Hotspot not needed."
    exit 0
fi

echo "No Wi-Fi connection. Enabling hotspot mode."

ip link set wlan0 down
ip addr flush dev wlan0
ip addr add 192.168.4.1/24 dev wlan0
ip link set wlan0 up
systemctl restart hostapd
systemctl restart dnsmasq
```

### Wi-Fi with wpa_supplicant

- Service: `wpa_supplicant@wlan0`
- Config: `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`
- Uses network `priority` to auto-select available options.

Rename default config if needed:
```sh
sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
sudo systemctl enable wpa_supplicant@wlan0
```

## GPIO Reserved for Shutdown

Connect a button between GPIO 21 and ground. In `/boot/config.txt`:

```sh
dtoverlay=gpio-shutdown,gpio_pin=21
```

## Additional Services

### 1. Monitor Serial Service

Path: `/etc/systemd/system/monitor-serial.service`
```ini
[Unit]
Description=LED Table Serial Monitor
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/monitor_serial.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
```sh
sudo systemctl enable monitor-serial.service
```

### 2. Status Server

Path: `/etc/systemd/system/status-server.service`
```ini
[Unit]
Description=Status Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/status_server.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
```sh
sudo systemctl enable status-server.service
```

### 3. Manage Effects

Path: `/etc/systemd/system/manage_effects.service`
```ini
[Unit]
Description=Effect Runner Service
After=multi-user.target

[Service]
ExecStart=/usr/local/bin/manage_effects.sh
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
```sh
sudo systemctl enable manage_effects.service
```

## Fallback Summary

- Both fallback services can be enabled and started via:

```sh
sudo systemctl enable wlan0-fallback.service
sudo systemctl enable eth0-fallback.service
sudo systemctl start wlan0-fallback.service
sudo systemctl start eth0-fallback.service
```
