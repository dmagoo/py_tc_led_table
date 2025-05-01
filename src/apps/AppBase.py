import time
import threading
import json

class AppBase:
    def __init__(self, table_api, params={}):
        """
        Initializes the app with the given table API and parameters.
        :param table_api: API to interact with the table (LEDs, sensors, etc.)
        :param params: Parameters specific to the app (e.g., effect settings)
        """
        self.table_api = table_api
        self.params = params
        self.tick = 0
        self.delta_time = 0.0
        self.running = True
        self._exit_event = threading.Event()
        # Keep track of touched node IDs
        self.touched_node_ids = []

    def run(self):
        """
        Main loop for the app. This is where the app will advance.
        The loop will be called with the current tick and delta time values.
        """

        last_time = time.time()
        while self.running:
            current_time = time.time()
            self.delta_time = current_time - last_time
            self.tick += 1
            last_time = current_time
            self.loop(self.tick, self.delta_time)
            time.sleep(0.005)  # Adjust for timing consistency

    def loop(self, tick, delta_time):
        """
        Child classes must implement this method.
        :param tick: Current tick count of the app.
        :param delta_time: Time elapsed since the last tick.
        """
        raise NotImplementedError("Each app must define its own loop method")

    def handle_touch_event(self, node_id, touched):
        """
        Handles the touch event for a specific node.
        This method is to be implemented by child apps for custom behavior.
        :param node_id: ID of the touched node
        :param touched: Boolean indicating whether the node was touched
        """
        if touched:
            if node_id not in self.touched_node_ids:
                self.touched_node_ids.insert(0, node_id)
                self.handle_node_touched(node_id)
        else:
            if node_id in self.touched_node_ids:
                self.touched_node_ids.remove(node_id)
                self.handle_node_untouched(node_id)

    def handle_node_touched(self, node_id):
        """
        Handle the event when a node is touched.
        This method should be overridden in child apps if needed.
        :param node_id: ID of the touched node
        """
        pass

    def handle_node_untouched(self, node_id):
        """
        Handle the event when a node is no longer touched.
        This method should be overridden in child apps if needed.
        :param node_id: ID of the untouched node
        """
        pass

    def stop(self):
        """
        Stop the app gracefully.
        """
        self.running = False
        self._exit_event.set()  # Signal the main loop to exit

    def wait_until_done(self):
        """
        Block until the app finishes.
        """
        self._exit_event.wait()  # Wait for stop() to signal that the loop should exit
