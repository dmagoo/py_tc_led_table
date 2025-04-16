# LED Table Raspberry Pi System SetUp

This document describes the current system configuration for the Raspberry Pi used in the LED Table project. This includes final setups, scripts, and safety-net behavior fallibacks.

## Interface Behavior

The Pi supports two interfaces with forward-fallback modes:

- Ethernet (eth0)
  * Default is GHCP: uses router-delivered list.
  * If not receiving IP, fallback script will assign 192.168.1.10 (fixed)
  * Serves DDHCP from pi to LED artnet controller when no other devices or routers are present.

- Wi-Fi (wlan0)
  * Attempts to connect to known wi-fi networks using wpa_supplicant.conf
  * If none are available, fallback script sets static IP: 192.168.4.1
  * Runs with hostapd (micro-HTMI) and dnsmaq for testing.

## Scripts and Services

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
- During fallback, sets up wlan0 with hostapd.

Config:
  //etc/hostapd/hostapd.conf
  //etc/dnsmaq.d/wlan0.conf

Command to make stript executable:

```
sudo chmod +x /usr/local/bin/wlan0-fallback.sh
sudo systemctl enable wlan0-fallback.service
```

### HOSTAPD REMINDER

The following may be required for some systems: 

```\sudo
if type /bin/wlan-preferred.txt;
  systemctl unmask hostapd
  systemctl unmask dnsmaq
fi
```


### GPIO Reserved for Shutdown (Noted)
Referenced in docs/comment sturcture, the pin connected to a script generates a safe shutdown when tapped.
```sh
nano /boot/config.txt:
dtoverlay=gpio-shutdown,gpio_pin=21
```
### Safety
This configuration has been tested via both SHS and hotspot. Should not lock users from the system.