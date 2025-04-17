import time

class EffectRunner:
    def __init__(self, effect_classes, table_api):
        self.effect_classes = effect_classes  # List of effect classes (e.g., [Snek, Ripple])
        self.table_api = table_api
        self.current_effect = None
        self.running = True

    def stop_current_effect(self):
        """ Stop the currently running effect gracefully and wait for cleanup """
        if self.current_effect:
            self.current_effect.stop()  # Stop the current effect
            self.current_effect.wait_until_done()  # Wait for it to finish cleaning up

    def switch_effect(self, effect_class=None, params=None):
        """ Switch to the next effect or stop the current effect if effect_class is None """
        if effect_class:
            self.stop_current_effect()
            self.current_effect = effect_class(self.table_api, **(params or {}))
            self.current_effect.run()  # Start the new effect
        else:
            # If effect_class is None, just stop the current effect
            self.stop_current_effect()

    def run(self):
        """ Start running the effects, switching every 30 seconds by default """
        while self.running:
            self.switch_effect()  # Switch to the next effect (or the one passed by the signal)
            time.sleep(30)  # Wait for 30 seconds before switching again
