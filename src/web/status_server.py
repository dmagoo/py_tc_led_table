# src/web/status_server.py
# Flask app entry point with status and effects routes

#!/usr/bin/env python3

from flask import Flask, jsonify
import socket
import subprocess
import os

app = Flask(__name__)

# Register blueprints
from routes.effects import effects_bp
app.register_blueprint(effects_bp)

def get_ip(interface):
    try:
        result = subprocess.check_output(
            ["ip", "-4", "addr", "show", interface],
            stderr=subprocess.DEVNULL
        ).decode()
        for line in result.splitlines():
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
    except Exception:
        return None

def get_interface_status(interface):
    try:
        output = subprocess.check_output(["cat", f"/sys/class/net/{interface}/operstate"])
        return output.decode().strip()
    except Exception:
        return "unknown"

def check_serial_monitor():
    process_check = os.system("systemctl is-active --quiet monitor-serial.service")
    return process_check == 0

@app.route("/status")
def status():
    return jsonify({
        "network": {
            "eth0": {
                "ip": get_ip("eth0"),
                "status": get_interface_status("eth0")
            },
            "wlan0": {
                "ip": get_ip("wlan0"),
                "status": get_interface_status("wlan0")
            }
        },
        "serial_monitor": {
            "status": "running" if check_serial_monitor() else "not running"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
