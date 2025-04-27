import time
import threading
from utils import wrgb_tuple_to_int
from .AppBase import AppBase

class TestApp(AppBase):
    def __init__(self, table_api, params={}):
        """
        Initializes the TestApp.
        :param table_api: The API to interact with the LED table (filled by AppBase)
        :param params: Parameters specific to the TestApp (e.g., effect settings)
        """
        super().__init__(table_api, params)
        self.flash_duration = 1.0  # Seconds to stay white before fading back
        self.fade_duration = 3.0   # Time it takes to fade back to black
        self.color = (255, 255, 255, 255)  # White color
        self.fade_color = (0, 0, 0, 0)  # Black color
        self.flash_start_time = None
        self.node_times = {}


    def loop(self, tick, delta_time):
        """
        Main loop for the TestApp. This method is called every tick to update the state.
        :param tick: Current tick count of the app.
        :param delta_time: Time elapsed since the last tick.
        """
        this_time = time.time()


        for node_id in self.node_times.copy().keys():
            node_timer =  self.node_times[node_id]
            elapsed_time = None
            if node_timer["start_time"] is None:
                node_timer["start_time"] = this_time

            elapsed_time = this_time - node_timer["start_time"]

            if not node_timer["fading"]:
                if elapsed_time >= self.flash_duration:
                    node_timer["fading"] = True
                    node_timer["start_time"] = this_time
                    self.send_node_color(node_timer)
            else:
                # Handle the fade-out effect
                if elapsed_time < self.fade_duration:
                    fade_percentage = elapsed_time / self.fade_duration
                    node_timer["color"] = self.fade_to_black(node_timer["color"], fade_percentage)
                    print(node_timer["color"])
                    self.send_node_color(node_timer)
                else:
                    node_timer["color"] = self.fade_color 
                    # Final fade to black
                    self.send_node_color(node_timer)
                    del self.node_times[node_id]

        self.table_api.refresh()

    def send_node_color(self, color):
        """
        Updates the node color. This method sends the color to the node.
        :param color: The color to set on the node (RGBA).
        """
        for node_id in self.node_times.keys():
            self.table_api.fillNode(node_id, wrgb_tuple_to_int(self.node_times[node_id]["color"]))

    def fade_to_black(self, color, percentage):
        """
        Fades a color towards black based on the given percentage.
        :param color: The current color (RGBA).
        :param percentage: A float between 0 and 1 representing the fade amount.
        :return: A new color, faded towards black.
        """
        return tuple(int(c * (1 - percentage)) for c in color)

    def handle_node_touched(self, node_id):
        """
        Handles the event when a node is touched.
        Immediately flashes the touched node white and starts the fade-out.
        """
        self.node_times[node_id] = {"fading": False, "start_time": False, "color": (255, 255, 255, 255)}

    def handle_node_untouched(self, node_id):
        """
        Handles the event when a node is no longer touched.
        No action for now, but can be extended in the future.
        """
        pass

# Run the TestApp as a drop-in with AppRunner
def main():
    led_table_config = add_controller_config(tc_led_table.LedTableConfig())
    tc_led_table.init(config=led_table_config)
    app = TestApp(tc_led_table)
    app.use_display = False  # No display needed for this test
    app.run()

if __name__ == "__main__":
    main()
