# src/web/routes/effects.py
# Blueprint for effect-related API routes

from flask import Blueprint, jsonify
from effect_registry import EFFECT_REGISTRY

effects_bp = Blueprint("effects", __name__, url_prefix="/effects")

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
