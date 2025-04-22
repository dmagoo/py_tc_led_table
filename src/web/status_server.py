# src/web/status_server.py
# Flask app entry point with status and effects routes

#!/usr/bin/env python3
from flask import Flask, jsonify, render_template
from config.settings import get_config_value
from communication.mqtt_client import setup_mqtt_client
from communication.message_manager import MessageManager

app = Flask(__name__, template_folder="templates", static_folder="static")

broker = get_config_value("FlaskApp", "mqtt_broker_address", "MQTT_BROKER_ADDRESS")
client_id = get_config_value("FlaskApp", "mqtt_client_id", "MQTT_CLIENT_ID")

mqtt_client = setup_mqtt_client(broker_address=broker, client_id=client_id)
message_manager = MessageManager(mqtt_client)

app.config["message_manager"] = message_manager


# Register blueprints
from web.api.effects import effects_bp
app.register_blueprint(effects_bp)

# Register blueprints
from web.api.status import status_bp
app.register_blueprint(status_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
