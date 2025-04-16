#!/usr/bin/env python3

from flask import Flask, jsonify
import socket
import subprocess

app = Flask(__name__)

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

@app.route("/status/network")
def network_status():
    return jsonify({
        "eth0": {
            "ip": get_ip("eth0"),
            "status": get_interface_status("eth0")
        },
        "wlan0": {
            "ip": get_ip("wlan0"),
            "status": get_interface_status("wlan0")
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
