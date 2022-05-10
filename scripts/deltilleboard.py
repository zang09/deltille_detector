#!/usr/bin/python3

import math
import numpy as np
import sys

from pyx import canvas, color
import polygon_utils as poly

from board_design import BoardDesign
from tags.deltags import delTag16h5, delTag25h7, delTag25h9, delTag36h9, delTag36h11
from shapely.ops import unary_union


family2code = {
    "delTag16h5": (delTag16h5, 16),
    "delTag25h7": (delTag25h7, 25),
    "delTag25h9": (delTag25h9, 25),
    "delTag36h9": (delTag36h9, 36),
    "delTag36h11": (delTag36h11, 36),
}

s60 = math.sqrt(3.0) / 2
c60 = 0.5


class DeltilleBoard:
    def __init__(self, board_id: int, board_design: BoardDesign, tag_id_offset: int = 0):
        if board_design.board_type != "deltille":
            print(
                f"[ERROR] Wrong board type {board_design.board_type} for DeltilleBoard")
            sys.exit(0)

        if board_design.tag_family not in family2code:
            print(
                f"[ERROR] \'{board_design.tag_family}\' is unavailable for Deltille!")
            print(
                f"\tUse one of the following families instead.\n\t{[f for f in family2code.keys()]}")
            sys.exit(0)

        self.board_id = board_id
        self.grid = np.array(board_design.grid)
        self.rows, self.cols = self.grid.shape
        self.size = board_design.size
        self.tag_family = board_design.tag_family
        self.codes, self.num_bits = family2code[self.tag_family]
        self.tag_id_offset = board_design.tag_id_offset + tag_id_offset
        self.tag_border = board_design.tag_border
        self.description = f'{self.board_id},{self.cols-1},{self.rows-1},{self.size}\n' +\
                           f'{self.tag_family},{self.tag_border}\n'

        # Internal
        self.bg_polygons = None
        self.fg_polygons = None
        self.corner_map = {}  # map (r,c) -> (tag_id, count)

        # Draw polygons
        tag_id = self.tag_id_offset
        for r in range(self.rows):
            for c in range(self.cols):
                t = self.grid[r, c]
                if t == 0:
                    continue
                elif t == 1:
                    self.draw_black_triangle(r, c)
                elif t == 2:
                    self.draw_deltag(r, c, tag_id)
                    tag_id += 1

        # Update description
        i_orig, j_orig = (1, 1)  # set (1, 1) as origin
        for (key, value) in self.corner_map.items():
            i, j = key
            tag_id, count = value
            if count == 3:
                # A valid corner should have been counted three times
                i_new, j_new = [i - i_orig, j - j_orig]
                x, y = self.ij_to_xy(i_new, j_new)
                self.description += f'{tag_id},{j_new},{i_new},{x},{y},0\n'

    def ij_to_xy(self, i, j):
        """Convert point index to location
        """
        return [(i * c60 + j) * self.size, i * s60 * self.size]

    def update_corner_map(self, i, j, tag_id):
        if (i, j) not in self.corner_map:
            self.corner_map[(i, j)] = (tag_id, 1)
        else:
            tag_id_prev, count = self.corner_map[(i, j)]
            self.corner_map[(i, j)] = (max(tag_id, tag_id_prev), count+1)

    def draw_black_triangle(self, i, j):
        x, y = self.ij_to_xy(i, j)

        # Deltag is expected to be drawn in an upright triangle
        poly_triangle = poly.polygon_triangle(x, y, self.size)

        # Add to background polygons
        if self.bg_polygons is None:
            self.bg_polygons = poly_triangle
        else:
            self.bg_polygons = unary_union([self.bg_polygons, poly_triangle])

        # Update corners
        self.update_corner_map(i, j, -1)
        self.update_corner_map(i, j + 1, -1)
        self.update_corner_map(i + 1, j, -1)

    def draw_deltag(self, i, j, tag_id):
        """Draw a DelTag in a given triangle at (i, j)\\
                /   \
               /     \
              /  /0\  \
             /  /123\  \
            /  /45678\  \
           /  /.....  \  \
          /  /_________\  \
         /   black border  \
        ---------------------
        """
        x, y = self.ij_to_xy(i, j)

        # Background is a black triangle
        bg_poly = poly.polygon_triangle(x, y, self.size)

        # Add to background polygons
        if self.bg_polygons is None:
            self.bg_polygons = bg_poly
        else:
            self.bg_polygons = unary_union([self.bg_polygons, bg_poly])

        sqrt_bits = round(math.sqrt(self.num_bits))
        one_bit_length = self.size / (sqrt_bits + self.tag_border * 3)
        border_thickness = self.tag_border * one_bit_length

        # Draw white bits
        tag_code = self.codes[tag_id]
        fg_poly = []
        for r in range(sqrt_bits):
            for c in range((sqrt_bits - 1 - r) * 2 + 1):
                bit = -c - r**2 + 2*r*sqrt_bits - 2*r + 2*sqrt_bits - 2
                # Note: left-most bit is the 0-th
                if tag_code & (1 << bit):
                    x_bit = x + 1.5 * border_thickness + \
                        one_bit_length * (r * c60 + (c + 1)//2)
                    y_bit = y + s60 * border_thickness + s60 * one_bit_length * r
                    if c % 2 == 0:
                        fg_poly.append(poly.polygon_triangle(
                            x_bit, y_bit, one_bit_length))
                    else:
                        fg_poly.append(poly.polygon_triangle60(
                            x_bit, y_bit, one_bit_length))
        fg_poly = unary_union(fg_poly)

        # Add to foreground polygons
        if self.fg_polygons is None:
            self.fg_polygons = fg_poly
        else:
            self.fg_polygons = unary_union([self.fg_polygons, fg_poly])

        # Update corners
        self.update_corner_map(i, j, tag_id)
        self.update_corner_map(i, j + 1, -1)
        self.update_corner_map(i + 1, j, -1)

    def draw_to_canvas(self, c: canvas.canvas):
        # Draw background polygons first
        if self.bg_polygons is not None:
            poly.draw_polygons(c, self.bg_polygons,
                               color.rgb.black, color.rgb.white)
        # Draw foreground polygons
        if self.fg_polygons is not None:
            poly.draw_polygons(c, self.fg_polygons,
                               color.rgb.white, color.rgb.black)

    def get_description(self):
        return self.description
