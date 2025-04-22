# src/web/routes/effects.py
# Blueprint for effect-related API routes
import sys

from flask import Blueprint, jsonify, request, current_app
from runner.effect_registry import EFFECT_REGISTRY
from communication.mqtt_client import publish_message

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

    if not effect_name or effect_name not in EFFECT_REGISTRY:
        return jsonify({"error": "Invalid effect"}), 400

    publish_message(message_manager.mqtt_client, "ledtable/effect/start", effect_name)

    return jsonify({"status": "ok", "effect": effect_name})
