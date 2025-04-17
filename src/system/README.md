
# LED Table Raspberry Pi System SetUp
This document describes the current system configuration for the Raspberry Pi used in the LED Table project. This includes final setups, scripts, and safety-net behavior fallbacks.

## Interface Behavior
The Pi supports two interfaces with forward-fallback modes:

- Ethernet (eth0)
  * Default is DDHCP: uses router-delivered list.
  * If not receiving IP from router, fallback script sets fixed IP to: 192.168.1.10
  * Serves DDHCP from pi to LED artnet controller when no other routers or devices present.

- Wi-Fi (wlan0)
  * Attempts to connect to known wi-fi networks using wpa_supplicant-wlan0.conf
  * If none are available, fallback script sets static IP: 192.168.4.1
  * Runs with hostapd and dnsmaq for testing.

## Scripts and Services

The system rely on simple, enabled systemds services to ensure fallback coverage without relying on NetworkManager. This is the structure:

### Ethernet Fallback
- /src/system/eth0-fallback.sh
- Static IP used: 192.168.1.10/24
- Dnsmaq conf: /etc/dnsmaq.d/eth0.conf
- Custom service: /src/system/eth0-fallback.service

Command to make script executable:

```
sudo chmod +x /usr/local/bin/eth0-fallback.sh
sudo systemctl enable eth0-fallback.service
```

### Wi-Fi Fallback
- /src/system/wlan0-fallback.sh
- Static IP used: 192.168.4.1/24
- During fallback, sets up wlan0 with hostapt, dnsmaq wiredup

Config:
  /etc/hostapd/hostapd.conf
  /etc/dnsmaq.d/wlan0.conf

Service: /src/system/wlan0-fallback.service

Script with latest checks:

```sh
connected=$(ip addr show $wlan0 | grep '"inet " | grep -v "192.168.4")
if [ -n "$connected" ]; then
    echo "Wi-Fi is connected. Hotspot not needed."
    exit 0
fi

echo "No Wi-Fi connection. Enabling hotspot mode."

ip link set $wlan0 down
ip addr flush dev $wlan0
ip addr add 192.168.4.1/24 dev $wlan0
ip link set $wlan0 up
systemctl restart hostapd
systemctl restart dnsmaq
```

### Wi-Fi WPE Config
Configuration for local wi-fi networks is now saved at:

      /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

__END_NETWORK__

### Wi-Fi Running with wpa_supplicant

- Wpa_supplicant is managed by systemd unit `wpa_supplicant@wlan0`
sudo systemctl enable wpa_supplicant@wlan0

- Config file must be named:
      /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

     (symlink from default conf to match with @wlan0 unit)  
    sudo mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant-wlan0.conf

## GPIO Reserved for Shutdown
Connect a button between gpio 21 and ground to safely shut down the system

```sh
nano /boot/config.txt:
dtoverlay=gpio-shutdown,gpio_pin=21
```

## Safety
The system will not default switch out of fallback modes during runtime unless manually explicitly set.

## Adding Additional Services:

### 1. **Monitor Serial Service**
Copy to: `/etc/systemd/system/monitor-serial.service`

```
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
Command to install:

```
sudo systemctl enable monitor-serial.service
```

### 2. **Status Server**
Copy to: `/etc/systemd/system/status-server.service`

```
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

Command to install:

```
sudo systemctl enable status-server.service
```

### 3. **Manage Effects**
Copy to: `/etc/systemd/system/manage_effects.service`

```
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

Command to install:

```
sudo systemctl enable manage_effects.service
```

### 4. **Wi-Fi & Ethernet Fallbacks**
- Follow instructions in `Wi-Fi Fallback` and `Ethernet Fallback` sections.
- These handle the fallback mechanism for network connectivity and DHCP.

```
sudo systemctl enable wlan0-fallback.service
sudo systemctl enable eth0-fallback.service
```

```
sudo systemctl start wlan0-fallback.service
sudo systemctl start eth0-fallback.service
```
