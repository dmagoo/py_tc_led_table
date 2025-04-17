import time
import threading
import signal
import sys

class EffectRunner:
    def __init__(self, effect_classes, table_api):
        print("initializing runner")
        self.effect_classes = effect_classes  # List of effect classes (e.g., [Snek, Ripple])
        self.table_api = table_api
        self.current_effect_index = -1  # Initialize the index
        self.current_effect = None
        self.running = True
        self.effect_thread = None

        # Set up signal handler to gracefully stop the script when receiving SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, self.handle_interrupt)

        self.switch_effect(self.get_next_effect())  # Start with the first effect

    def stop_current_effect(self):
        """ Stop the currently running effect gracefully and wait for cleanup """
        if self.current_effect:
            print("stopping old effect")
            self.current_effect.stop()  # Stop the current effect
            self.current_effect.wait_until_done()  # Wait for it to finish cleaning up

    def get_next_effect(self):
        self.current_effect_index = (self.current_effect_index + 1) % len(self.effect_classes)
        return self.effect_classes[self.current_effect_index]

    def switch_effect(self, effect_class=None, params=None):
        """ Switch to the next effect or stop the current effect if effect_class is None """
        print("switching effects")
        if effect_class:
            self.stop_current_effect()
            self.current_effect = effect_class(self.table_api, **(params or {}))
            self.current_effect.use_display = False
            print("starting new effect")
            # Run the effect in a separate thread to avoid blocking
            self.effect_thread = threading.Thread(target=self.current_effect.run)
            self.effect_thread.start()
        else:
            # If effect_class is None, just stop the current effect
            self.stop_current_effect()

    def run(self):
        print("starting effect runner")
        """ Start running the effects, switching every 30 seconds by default """
        while self.running:
            self.switch_effect(self.get_next_effect())  # Switch to the next effect
            time.sleep(30)  # Wait for 30 seconds before switching again

    def handle_interrupt(self, sig, frame):
        """ Gracefully handle the interrupt (Ctrl+C) and stop the effect runner """
        print("Interrupt received. Stopping EffectRunner...")
        self.running = False
        if self.effect_thread:
            self.effect_thread.join()  # Wait for the effect thread to finish cleanly
        print("EffectRunner stopped.")
        sys.exit(0)  # Exit cleanly
