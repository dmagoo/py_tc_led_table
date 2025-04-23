# src/web/routes/effects.py
# Blueprint for effect-related API routes
import sys
import json
from flask import Blueprint, jsonify, request, current_app
from runner.effect_registry import EFFECT_REGISTRY
from communication.mqtt_client import publish_message
from web.decorators import track_latest_message_from_topic

effects_bp = Blueprint("effects", __name__, url_prefix="/api/effects")

@effects_bp.route("/", methods=["GET"])
def list_effects():
    effects = []
    for name, meta in EFFECT_REGISTRY.items():
        if not meta.get("suppressFromWebUI"):
            effects.append({
                "name": name,
                "params": meta.get("params", {})
            })
    return jsonify(effects)


@effects_bp.route("/start", methods=["POST"])
def start_effect():
    message_manager = current_app.config["message_manager"]
    data = request.get_json()
    effect_name = data.get("effect")
    params = data.get("params", {})

    if not effect_name or effect_name not in EFFECT_REGISTRY:
        return jsonify({"error": "Invalid effect"}), 400

    payload = {
        "effect": effect_name,
        "params": params
    }

    publish_message(message_manager.mqtt_client, "ledtable/effect/start", json.dumps(payload))

    return jsonify({"status": "ok", "effect": effect_name})

@effects_bp.route("/stop", methods=["POST"])
def stop_effect():
    message_manager = current_app.config["message_manager"]
    payload = {}

    publish_message(message_manager.mqtt_client, "ledtable/effect/stop", json.dumps(payload))

    return jsonify({"status": "ok"})

@effects_bp.route("/status", methods=["GET"])
@track_latest_message_from_topic("ledtable/effect/status")
def get_effect_status():
    message_manager = current_app.config.get("message_manager")
    if not message_manager:
        return jsonify({"error": "No message manager"}), 500

    latest = message_manager.get_latest_message_from_topic("ledtable/effect/status")
    if not latest:
        return jsonify({"status": "unknown"}), 404

    return jsonify(latest)
