from enum import Enum
import numpy as np
import struct

def rgb_tuple_to_int(color_tuple):
    # Unpack the RGB components from the tuple
    r, g, b = color_tuple
    # Shift the components and combine them into a 32-bit integer
    # The first 8 bits are 0, followed by red, green, and blue components
    color_int = (r << 16) | (g << 8) | b
    return color_int

def wrgb_tuple_to_int(color_tuple):
    # Unpack the RGB components from the tuple
    w, r, g, b = color_tuple
    # Shift the components and combine them into a 32-bit integer
    # The first 8 bits are 0, followed by red, green, and blue components
    color_int = (w << 24) | (r << 16) | (g << 8) | b
    return color_int


def int_to_rgb_tuple(color_int):
    # Extract the RGB components by shifting and masking with 0xFF
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r, g, b)

def int_to_wrgb_tuple(color_int):
    # Extract the WRGB components by shifting and masking with 0xFF
    w = (color_int >> 24) & 0xFF
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (w, r, g, b)

# return a numpy array of 32-bit ints, representing the color
def fill_between(length, index_a, index_b, rgb_tuple, direction='clockwise'):
    color = rgb_tuple_to_int(rgb_tuple)
    arr = np.zeros(length)  
    
    if direction == 'clockwise':
        if index_a <= index_b:
            arr[index_a:index_b + 1] = color
        else:
            # Fill from index_a to the end and from the start to index_b
            arr[index_a:] = color
            arr[:index_b + 1] = color
    elif direction == 'counter_clockwise':
        if index_a >= index_b:
            arr[index_b:index_a + 1] = color
        else:
            # Fill from index_b to the end and from the start to index_a
            arr[index_b:] = color
            arr[:index_a + 1] = color
    
    return arr


def unpack_artnet_data_to_rgb_2dOLD(data, pixels_per_node=8, drop_w=False):
    """ Chunk the list of RGB tuples into sub-lists of length 'pixels_per_node' """
    # Initialize the list to hold the RGB or WRGB tuples
    tuples = []

    # Iterate over the data in steps of 4 bytes (32 bits)
    for i in range(0, len(data), 4):
        # Unpack 4 bytes at a time, capturing W, R, G, and B components
        w, r, g, b = struct.unpack('4B', data[i:i+4])

        # Append the tuple to the list, including 'W' if keep_w is True
        if drop_w:
            tuples.append((r, g, b))
        else:
            tuples.append((w, r, g, b))

    # Chunk the list of tuples into sub-lists of length 'pixels_per_node'
    tuple_chunks = [tuples[i:i + pixels_per_node] for i in range(0, len(tuples), pixels_per_node)]
    return tuple_chunks

class ARTNET_PACKET_FORMAT(Enum):
    RGBW = 1
    WRGB = 2
    GRBW = 3

def rewire_pixel(color_tuple, format):
    """ take a tuple of color components and return them as
        a normalized WRGB
    """
    (a,b,c,d) = color_tuple
    return {
        ARTNET_PACKET_FORMAT.WRGB: (a,b,c,d),
        ARTNET_PACKET_FORMAT.GRBW: (d,b,a,c),
        ARTNET_PACKET_FORMAT.RGBW: (d,a,b,c)
    }[format]

def unpack_artnet_data_to_rgb_2d(data, pixels_per_node=8, format=ARTNET_PACKET_FORMAT.GRBW):
    """ Chunk the list of RGB tuples into sub-lists of length 'pixels_per_node' """
    # Initialize the list to hold the RGB or WRGB tuples
    tuples = []

    # Iterate over the data in steps of 4 bytes (32 bits)
    for i in range(0, len(data), 4):
        # Unpack 4 bytes at a time, capturing W, R, G, and B components
        color_tuple = struct.unpack('4B', data[i:i+4])
        tuples.append(rewire_pixel(color_tuple, format))

    # Chunk the list of tuples into sub-lists of length 'pixels_per_node'
    tuple_chunks = [tuples[i:i + pixels_per_node] for i in range(0, len(tuples), pixels_per_node)]
    return tuple_chunks


def gamma_correct(value, gamma):
    return value ** gamma

def apply_gamma_correction(color, gamma_r, gamma_g, gamma_b):
    r_corrected = int(gamma_correct(color[0] / 255, gamma_r) * 255)
    g_corrected = int(gamma_correct(color[1] / 255, gamma_g) * 255)
    b_corrected = int(gamma_correct(color[2] / 255, gamma_b) * 255)
    return (r_corrected, g_corrected, b_corrected)

# Example usage:
"""
gamma_r = 2.4  # Gamma value for the red component
gamma_g = 2.2  # Gamma value for the green component
gamma_b = 2.8  # Gamma value for the blue component
color = (r, g, b)  # Your RGB color values
corrected_color = apply_gamma_correction(color, gamma_r, gamma_g, gamma_b)
"""