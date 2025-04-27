# src/web/routes/apps.py
# Blueprint for app-related API routes
import sys
import json
from flask import Blueprint, jsonify, request, current_app
from runner.app_registry import APP_REGISTRY
from communication.mqtt_client import publish_message
from web.decorators import track_latest_message_from_topic

apps_bp = Blueprint("apps", __name__, url_prefix="/api/apps")

@apps_bp.route("/", methods=["GET"])
def list_apps():
    apps = []
    for name, meta in APP_REGISTRY.items():
        if not meta.get("suppressFromWebUI"):
            apps.append({
                "name": name,
                "params": meta.get("params", {})
            })
    return jsonify(apps)


@apps_bp.route("/start", methods=["POST"])
def start_app():
    message_manager = current_app.config["message_manager"]
    data = request.get_json()
    app_name = data.get("app")
    params = data.get("params", {})

    if not app_name or app_name not in APP_REGISTRY:
        return jsonify({"error": "Invalid app"}), 400

    payload = {
        "app": app_name,
        "params": params
    }

    publish_message(message_manager.mqtt_client, "ledtable/app/start", json.dumps(payload))

    return jsonify({"status": "ok", "app": app_name})

@apps_bp.route("/stop", methods=["POST"])
def stop_app():
    message_manager = current_app.config["message_manager"]
    payload = {}

    publish_message(message_manager.mqtt_client, "ledtable/app/stop", json.dumps(payload))

    return jsonify({"status": "ok"})

@apps_bp.route("/status", methods=["GET"])
@track_latest_message_from_topic("ledtable/app/status")
def get_app_status():
    message_manager = current_app.config.get("message_manager")
    if not message_manager:
        return jsonify({"error": "No message manager"}), 500

    latest = message_manager.get_latest_message_from_topic("ledtable/app/status")
    if not latest:
        return jsonify({"status": "unknown"}), 404

    return jsonify(latest)
