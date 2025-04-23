# EffectRunner.py
# Manages effect execution, switching logic, and status effects

import os
import time
import threading
import signal
import sys
import json
from effect_registry import EFFECT_REGISTRY

STATUS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "status_config.json")

class EffectRunner:
    def __init__(self, table_api, message_manager):
        self.table_api = table_api
        self.effect_classes = EFFECT_REGISTRY
        self.effect_order = [k for k in self.effect_classes if not self.effect_classes[k].get("suppressFromWebUI")]
        self.current_effect_index = -1
        self.current_effect = None
        self.effect_thread = None
        self.running = True
        self.status = None
        self.message_manager = message_manager
        self.status_config = self.load_status_config()
        self.demo_mode = False  # Disable cycling by default

        self.current_effect_name = None
        self.current_params = {}

        self.status_interval = 5     # seconds
        self.switch_interval = 30    # seconds

        signal.signal(signal.SIGINT, self.handle_interrupt)
        self.set_status("idle", run_effect=True)

        self.message_manager.register_topic("ledtable/effect/start")
        self.message_manager.mqtt_client.message_callback_add("ledtable/effect/start", self.handle_effect_start)
        self.message_manager.register_topic("ledtable/effect/stop")
        self.message_manager.mqtt_client.message_callback_add("ledtable/effect/stop", self.handle_effect_stop)

    def load_status_config(self):
        try:
            with open(STATUS_CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print(str(e))
            return {}

    def handle_effect_start(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            effect_name = payload.get("effect")
            params = payload.get("params", {})

            if effect_name in self.effect_classes:
                self.switch_effect(effect_name, params=params)
            else:
                print(f"Ignored unknown effect: {effect_name}")

        except Exception as e:
            print(f"Invalid effect message: {e}")
            
    def handle_effect_stop(self, client, userdata, msg):
        self.stop_current_effect()


    def stop_current_effect(self):
        if self.current_effect:
            self.current_effect.stop()
            self.current_effect.wait_until_done()

    def get_next_effect_name(self):
        self.current_effect_index = (self.current_effect_index + 1) % len(self.effect_order)
        return self.effect_order[self.current_effect_index]

    def switch_effect(self, effect_name=None, params=None):
        print("SWTICH")
        print(effect_name)
        if effect_name:
            self.set_status("active", run_effect=False)
            self.stop_current_effect()
            effect_class = self.effect_classes[effect_name]["class"]
            self.current_effect_name = effect_name
            self.current_params = params or {}
            self.current_effect = effect_class(self.table_api, params=self.current_params)
            self.current_effect.use_display = False
            self.effect_thread = threading.Thread(target=self.current_effect.run)
            self.effect_thread.start()
            self.publish_status()
        else:
            self.stop_current_effect()

    def publish_status(self):
        if self.message_manager:
            self.message_manager.publish(
                "ledtable/effect/status",
                {
                    "eventType": "effect_status",
                    "effect": self.current_effect_name,
                    "params": self.current_params
                }
            )

    def set_status(self, status_name, run_effect=True):
        self.status = status_name
        status_entry = self.status_config.get(status_name)
        if status_entry and run_effect:
            self.switch_effect(
                effect_name=status_entry["effect"],
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
                self.switch_effect(self.get_next_effect_name())
                last_switch = now
            if (now - last_status) >= self.status_interval:
                self.broadcast_current_status()
                last_status = now
            time.sleep(0.5)

    def handle_interrupt(self, sig, frame):
        self.running = False
        if self.effect_thread:
            self.effect_thread.join()
        sys.exit(0)
