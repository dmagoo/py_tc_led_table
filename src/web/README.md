yh# Web Server - Status API for LED Table

This directory contains a Flask-served application that reports network status of the Raspberry Pi device, available at `/status/network` on port 0880 in default configuration.

- Provides JSON-style output of connected interfaces eth0 waln0
- Serves the page via `localhost:8080` (or via IP on the network)
- Service file: `status-server.service` under `/etc/systemd/s`
- Runs as user `tcledtable` in user-space
- Code lives in `src/system/web/status_server.py`

## Future Steps: Nginx Proxy

This Section will later be replaced with a nginx reverse proxy config to reroute all traffic to the Flask app on port 8080.

- Flask app is also future-working without root user permissions.
- Port 80 rediscussed in favor of 2080 in the future
- Reverse from port 80 to 2080 is deferred with nginx for later

## Usage

app reached via: http://localhost:8080/status/network
CROSS-device safe: curl -s or browser can test the ENDPOINT directly.

## Starting the Server

Requires `status-server.service` in /etc/systemd/system/

To enable and run it:

```
sudo systemctl reload
sudo systemctl restart status-server.service
```

## Note

This config assumes interfaces are read-only and that `app.run` does not listen on stddin or manage other states.ڱ^r^?D@0I