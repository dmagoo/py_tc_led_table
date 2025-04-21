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
    def __init__(self, table_api):
        self.table_api = table_api
        self.effect_classes = EFFECT_REGISTRY
        self.effect_order = [k for k in self.effect_classes if not self.effect_classes[k].get("suppressFromWebUI")]
        self.current_effect_index = -1
        self.current_effect = None
        self.effect_thread = None
        self.running = True
        self.status = None
        self.status_config = self.load_status_config()
        self.demo_mode = False  # Disable cycling by default

        signal.signal(signal.SIGINT, self.handle_interrupt)
        self.set_status("idle", run_effect=True)

    def load_status_config(self):
        try:
            with open(STATUS_CONFIG_PATH, "r") as f:
                return json.load(f)
        except Exception as e:
            print("bad")
            print(str(e))
            return {}

    def stop_current_effect(self):
        if self.current_effect:
            self.current_effect.stop()
            self.current_effect.wait_until_done()

    def get_next_effect_name(self):
        self.current_effect_index = (self.current_effect_index + 1) % len(self.effect_order)
        return self.effect_order[self.current_effect_index]

    def switch_effect(self, effect_name=None, params=None):
        if effect_name:
            self.set_status("active", run_effect=False)
            self.stop_current_effect()
            effect_class = self.effect_classes[effect_name]["class"]
            #self.current_effect = effect_class(self.table_api, **(params or {}))
            self.current_effect = effect_class(self.table_api, params=(params or {}))

            self.current_effect.use_display = False
            self.effect_thread = threading.Thread(target=self.current_effect.run)
            self.effect_thread.start()
        else:
            self.stop_current_effect()

    def set_status(self, status_name, run_effect=True):
        self.status = status_name
        status_entry = self.status_config.get(status_name)
        print("setting status")
        print(status_name)
        print(status_entry)
        print(self.status_config)
        if status_entry and run_effect:
            print("running effect")
            print(status_entry["effect"])
            self.switch_effect(
                effect_name=status_entry["effect"],
                params=status_entry.get("params", {})
            )

    def run(self):
        while self.running:
            if self.demo_mode:
                self.switch_effect(self.get_next_effect_name())
            time.sleep(30)

    def handle_interrupt(self, sig, frame):
        self.running = False
        if self.effect_thread:
            self.effect_thread.join()
        sys.exit(0)
