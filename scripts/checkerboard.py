#!/usr/bin/python3

import math
import numpy as np
import sys

from pyx import canvas, color
import polygon_utils as poly

from board_design import BoardDesign
from tags.apriltags import aprilTag16h5, aprilTag25h7, aprilTag25h9, aprilTag36h9, aprilTag36h11
from shapely.ops import unary_union


family2code = {
    "aprilTag16h5": (aprilTag16h5, 16),
    "aprilTag25h7": (aprilTag25h7, 25),
    "aprilTag25h9": (aprilTag25h9, 25),
    "aprilTag36h9": (aprilTag36h9, 36),
    "aprilTag36h11": (aprilTag36h11, 36),
}


class AprilCheckerBoard:
    def __init__(self, board_id: int, board_design: BoardDesign, tag_id_offset: int = 0):
        if board_design.board_type != "checkerboard":
            print(
                f"[ERROR] Wrong board type {board_design.board_type} for AprilCheckerBoard")
            sys.exit(0)

        if board_design.tag_family not in family2code:
            print(
                f"[ERROR] \'{board_design.tag_family}\' is unavailable for checkerboard!")
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
                    self.draw_black_square(r, c)
                elif t == 2:
                    self.draw_apriltag(r, c, tag_id)
                    tag_id += 1

        # Update description
        i_orig, j_orig = (1, 1)  # set (1, 1) as origin
        for (key, value) in self.corner_map.items():
            i, j = key
            tag_id, count = value
            if count == 2:
                # A valid corner should have been counted twice
                i_new, j_new = [i - i_orig, j - j_orig]
                x, y = self.ij_to_xy(i_new, j_new)
                self.description += f'{tag_id},{j_new},{i_new},{x},{y},0\n'

    def ij_to_xy(self, i, j):
        """Convert point index to location"""
        return [j * self.size, i * self.size]

    def update_corner_map(self, i, j, tag_id):
        if (i, j) not in self.corner_map:
            self.corner_map[(i, j)] = (tag_id, 1)
        else:
            tag_id_prev, count = self.corner_map[(i, j)]
            self.corner_map[(i, j)] = (max(tag_id, tag_id_prev), count+1)

    def draw_black_square(self, i, j):
        x, y = self.ij_to_xy(i, j)
        poly_square = poly.polygon_square(x, y, self.size)

        # Add to background polygons
        if self.bg_polygons is None:
            self.bg_polygons = poly_square
        else:
            self.bg_polygons = unary_union([self.bg_polygons, poly_square])

        # Update corners
        self.update_corner_map(i, j, -1)
        self.update_corner_map(i, j + 1, -1)
        self.update_corner_map(i + 1, j, -1)
        self.update_corner_map(i + 1, j + 1, -1)

    def draw_apriltag(self, i, j, tag_id):
        """Draw an AprilTag in a given quad at (i, j)
        ---------------
        | black border|
        |   -------   |
        |   |01234|   |
        |   |567..|<---- each location is filled by black(0) or white(1)
        |   |.....|   |
        |   -------   |
        |             |
        ---------------

        Args:
            i (int): quad location
            j (int): quad location
            tag_id (int): tag index
        """
        x, y = self.ij_to_xy(i, j)

        sqrt_bits = round(math.sqrt(self.num_bits))
        one_bit_length = self.size / (sqrt_bits + self.tag_border * 2)
        border_thickness = self.tag_border * one_bit_length

        # Background is a black square
        bg_poly = poly.polygon_square(x, y, self.size)

        # Add to background polygons
        if self.bg_polygons is None:
            self.bg_polygons = bg_poly
        else:
            self.bg_polygons = unary_union([self.bg_polygons, bg_poly])

        # Draw white bits
        # Note: left-most bit is the 0-th (see the fig above)
        tag_code = self.codes[tag_id]
        fg_poly = []
        for r in range(sqrt_bits):
            for c in range(sqrt_bits):
                bit = sqrt_bits - 1 + r * sqrt_bits - c
                if tag_code & (1 << bit):
                    fg_poly.append(poly.polygon_square(
                        x + border_thickness + c * one_bit_length,
                        y + border_thickness + r * one_bit_length,
                        one_bit_length
                    ))
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
        self.update_corner_map(i + 1, j + 1, -1)

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
