# src/web/api/services.py
# Blueprint for managing systemd services

import subprocess
from flask import Blueprint, jsonify, request
from system.service_registry import SERVICE_REGISTRY

services_bp = Blueprint("services", __name__, url_prefix="/api/services")

def get_service_status(name):
    try:
        result = subprocess.run(["sudo", "systemctl", "is-active", name], capture_output=True, text=True, timeout=2)
        return result.stdout.strip()
    except Exception as e:
        return f"error: {e}"

@services_bp.route("/", methods=["GET"])
def list_services():
    result = []
    for name, meta in SERVICE_REGISTRY.items():
        status = get_service_status(name)
        result.append({
            "name": name,
            "label": meta["label"],
            "status": status,
            "controllable": meta["controllable"]
        })
    return jsonify(result)

@services_bp.route("/<name>/<action>", methods=["POST"])
def control_service(name, action):
    if name not in SERVICE_REGISTRY:
        return jsonify({"error": "Unauthorized service"}), 400
    if not SERVICE_REGISTRY[name]["controllable"]:
        return jsonify({"error": "Service not controllable"}), 403
    if action not in {"start", "stop", "restart"}:
        return jsonify({"error": "Invalid action"}), 400

    try:
        subprocess.run(["sudo", "systemctl", action, name], check=True, timeout=5)
        status = get_service_status(name)
        return jsonify({"success": True, "name": name, "action": action, "status": status})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": str(e)})
