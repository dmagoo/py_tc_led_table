# src/pygame/TableDisplay.py
import pygame
import pygame.freetype
import time
import random
import math
import numpy as np

from models.table import Table
from models.node import Node

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1125
NODE_COUNT = 37
BLACK = (0, 0, 0)
SCREEN_BACKGROUND = (72,46,33)
RING_BACKGROUND = (10,20,20)

import numpy as np

circle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 165, 0)]

class TableDisplay:
    def __init__(self, table_api):

        self.broadcast = False

        pygame.init()
        pygame.font.init()

        self.running = True
        self.max_frame_rate = 100
        self.clock = pygame.time.Clock()
        self.tick_count = 0
        self.current_frame_rate = 0
        self.last_api_refresh = time.time()
        self.last_stats_collection = time.time()
        self.tick_count = 0
        self.table_api = table_api
        self.setup_display()
        self.setup_table_model()
        self.screen_background_color = SCREEN_BACKGROUND
        self.event_list = []

    def setup_display(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Set your desired window size
        self.base_font = pygame.font.SysFont('default', 30)

    def setup_table_model(self):
        self.node_radius = SCREEN_HEIGHT/14
        self.node_ring_thickness = self.node_radius / 5
        self.table = Table(self.node_radius)  # Assuming Table class handles the structure of your LED table
        self.node_id_list = self.table_api.listNodeIds()

        xy_tuples = []

        for node_id in self.node_id_list:
            coord = self.table_api.getCartesian2dCoordinate(node_id)
            # cartesian position
            self.table.addNode(Node(node_id, coord, self.node_radius))
            xy_tuples.append((coord.getX(), coord.getY()))

        #get min and max x/y from types so we can scale to screen
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for x, y in xy_tuples:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

        # Calculate the scaling factors for x and y
        x_scale = (SCREEN_WIDTH - 2 * self.node_radius) / (max_x - min_x)
        y_scale = (SCREEN_HEIGHT - 2 * self.node_radius) / (max_y - min_y)

        # Normalize the coordinates using the scaling factors and node radius
        self.node_positions = [(int((x - min_x) * x_scale + self.node_radius),
                                int((y - min_y) * y_scale + self.node_radius))
                                for x, y in xy_tuples]

        max_y_scaled = (max_y - min_y) * y_scale + 2 * self.node_radius
        self.node_positions = [(int((x - min_x) * x_scale + self.node_radius),
                                (max_y_scaled) - int((y - min_y) * y_scale + self.node_radius))
                                for x, y in xy_tuples]


        # Calculate positions for the eight circles using numpy
        angle = np.linspace(math.pi / 2, math.pi / 2 - 2 * math.pi, 8, endpoint=False)
        radius = self.node_radius - (self.node_ring_thickness / 2)
        self.x_positions = radius * np.cos(angle)
        self.y_positions = -radius * np.sin(angle)  # Invert the y-coordinates

    def get_node_id_from_pos(self, pos, radius=None):
        radius = radius if radius is not None else self.node_radius
        x, y = pos
        for node_id, (node_x, node_y) in enumerate(self.node_positions):
            distance = ((node_x - x) ** 2 + (node_y - y) ** 2) ** 0.5
            if distance <= radius:
                return node_id
        return None

    def tick(self):
        pass

    def update_display(self):
        self.screen.fill(self.screen_background_color)  # Clear the screen with black
        for node in self.table.nodes:
            node_bg = (100,0,0) if node.touch_value > 50 else BLACK
            pygame.draw.circle(self.screen, RING_BACKGROUND, self.node_positions[node.id], node.radius)  # Example of drawing a node
            pygame.draw.circle(self.screen, node_bg, self.node_positions[node.id], node.radius-self.node_ring_thickness)  # Example of drawing a node
            if node.colors:
                for i, color in enumerate(node.colors_rgb):
                    pixel_center = (self.node_positions[node.id][0]+int(self.x_positions[i]),self.node_positions[node.id][1]+int(self.y_positions[i]))
                    pygame.draw.circle(self.screen, color, pixel_center, 5)  # Adjust radius as needed
            else:
                for i, color in enumerate(circle_colors):
                    pixel_center = (self.node_positions[node.id][0]+int(self.x_positions[i]),self.node_positions[node.id][1]+int(self.y_positions[i]))
                    pygame.draw.circle(self.screen, color[0:3], pixel_center, 5)  # Adjust radius as needed

            node_label = self.base_font.render("id: " + str(node.id), True, (100,80,0))
            coord = self.table_api.getCubeCoordinate(node.id)

            coord_label = self.base_font.render("qrs: " + str(coord.getQ()) + "," + str(coord.getR()) + "," + str(coord.getS()), True, (100,120,80))
            self.screen.blit(node_label, self.node_positions[node.id])
            self.screen.blit(coord_label, [p-40 for p in self.node_positions[node.id]])

    def update_stats(self):
        current_time = time.time()
        delta_time = current_time - self.last_stats_collection
        self.last_stats_collection = current_time
        if delta_time > 0:
            self.current_frame_rate = 1.0 / delta_time
        #    if self.tick_count % 100 == 0:
        #        print(f"--------------------------------------------- Current Frame Rate: {self.current_frame_rate:.2f} FPS") 

    def quit(self):
        pass

    def run(self):
        while self.running:
            self.event_list = pygame.event.get()

            for event in self.event_list:
                if event.type == pygame.QUIT:
                    self.running = False

            self.tick()
            self.tick_count += 1

            self.update_display()
            pygame.display.flip()

            self.clock.tick(self.max_frame_rate)  # Cap the frame rate
            self.update_stats()
        self.quit()
        pygame.quit()

# You might need additional methods for loading data, handling input, etc.
