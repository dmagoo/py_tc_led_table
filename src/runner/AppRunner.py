# AppRunner.py
# Manages app execution, switching logic, and status apps

import os
import time
import threading
import signal
import sys
import json
from app_registry import APP_REGISTRY

STATUS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "status_config.json")

class AppRunner:
    def __init__(self, table_api, message_manager):
        self.table_api = table_api
        self.app_classes = APP_REGISTRY
        self.app_order = [k for k in self.app_classes if not self.app_classes[k].get("suppressFromWebUI")]
        self.current_app_index = -1
        self.current_app = None
        self.app_thread = None
        self.running = True
        self.status = None
        self.message_manager = message_manager
        self.status_config = self.load_status_config()
        self.demo_mode = False  # Disable cycling by default

        self.current_app_name = None
        self.current_params = {}

        self.status_interval = 5     # seconds
        self.switch_interval = 30    # seconds

        signal.signal(signal.SIGINT, self.handle_interrupt)
        self.set_status("idle", run_app=True)

        self.message_manager.register_topic("ledtable/app/start")
        self.message_manager.mqtt_client.message_callback_add("ledtable/app/start", self.handle_app_start)
        self.message_manager.register_topic("ledtable/app/stop")
        self.message_manager.mqtt_client.message_callback_add("ledtable/app/stop", self.handle_app_stop)

        self.last_touch_times = {}  # (nodeId, touched) -> timestamp
        self.debounce_interval = 0.1  # seconds
        # not needed because we are not saving last-messages for later retrieval
        #self.message_manager.register_topic("ledtable/sensor/touch_event")
        self.message_manager.mqtt_client.register_listener("ledtable/sensor/touch_event", self.handle_touch_message)
        # self.message_manager.mqtt_client.message_callback_add("ledtable/sensor/touch_event", self.handle_touch_message)

    def handle_touch_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            node_id = payload["nodeId"]
            touched = payload["touched"]
            now = time.time()
            key = (node_id, touched)
            last_time = self.last_touch_times.get(key, 0)
            if (now - last_time) >= self.debounce_interval:
                self.last_touch_times[key] = now
                if self.current_app and hasattr(self.current_app, "handle_touch_event"):
                    self.current_app.handle_touch_event(node_id, touched)

        except Exception as e:
            print(f"Error handling touch message: {e}", flush=True)
            sys.exit(0)

    def load_status_config(self):
        try:
            with open(STATUS_CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(str(e))
            return {}

    def handle_app_start(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            app_name = payload.get("app")
            params = payload.get("params", {})

            if app_name in self.app_classes:
                self.switch_app(app_name, params=params)
            else:
                print(f"Ignored unknown app: {app_name}")

        except Exception as e:
            print(f"Invalid app message: {e}")
            
    def handle_app_stop(self, client, userdata, msg):
        self.stop_current_app()


    def stop_current_app(self):
        if self.current_app:
            self.current_app.stop()
            self.current_app.wait_until_done()

    def get_next_app_name(self):
        self.current_app_index = (self.current_app_index + 1) % len(self.app_order)
        return self.app_order[self.current_app_index]

    def switch_app(self, app_name=None, params=None):
        print("Switching app", app_name)
        if app_name:
            self.set_status("active", run_app=False)
            self.stop_current_app()
            app_class = self.app_classes[app_name]["class"]
            self.current_app_name = app_name
            self.current_params = params or {}
            self.current_app = app_class(self.table_api, params=self.current_params)
            self.current_app.use_display = False
            self.app_thread = threading.Thread(target=self.current_app.run)
            self.app_thread.start()
            self.publish_status()
        else:
            self.stop_current_app()

    def publish_status(self):
        if self.message_manager:
            self.message_manager.publish(
                "ledtable/app/status",
                {
                    "eventType": "app_status",
                    "app": self.current_app_name,
                    "params": self.current_params
                }
            )

    def set_status(self, status_name, run_app=True):
        self.status = status_name
        status_entry = self.status_config.get(status_name)
        if status_entry and run_app:
            self.switch_app(
                app_name=status_entry["app"],
                params=status_entry.get("params", {})
            )

    def broadcast_current_status(self):
        self.publish_status()

    def run(self):
        last_status = 0
        last_switch = 0
        while self.running:
            now = time.time()
            if self.demo_mode and (now - last_switch) >= self.switch_interval:
                self.switch_app(self.get_next_app_name())
                last_switch = now
            if (now - last_status) >= self.status_interval:
                self.broadcast_current_status()
                last_status = now
            time.sleep(0.5)

    def handle_interrupt(self, sig, frame):
        self.running = False
        if self.app_thread:
            self.app_thread.join()
        sys.exit(0)
