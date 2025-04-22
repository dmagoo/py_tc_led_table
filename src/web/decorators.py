# src/web/decorators.py
# Provides Flask decorators for MQTT integration

from functools import wraps
from flask import current_app

def track_latest_message_from_topic(topic):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            message_manager = current_app.config.get("message_manager")
            if message_manager:
                message_manager.track_latest_message_from_topic(topic)
            return f(*args, **kwargs)
        return wrapped
    return decorator
