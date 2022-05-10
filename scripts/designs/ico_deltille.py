#!/usr/bin/python3

import copy
import numpy as np

from board_design import BoardDesign, adjust_tag_id_offsets
from typing import List


def ico_deltille() -> List[BoardDesign]:
    """20 equilateral deltille boards for icosahedron"""
    # ↑ r                           ↑ y            ↗ r
    # |1 0 0 0 0 0 0 0 0 0 0 0 0  = |             ▲
    # |1 1 0 0 0 0 0 0 0 0 0 0 0  = |            ▲ ▲
    # |1 2 1 0 0 0 0 0 0 0 0 0 0  = |           ▲ T ▲
    # |1 1 1 1 0 0 0 0 0 0 0 0 0  = |          ▲ ▲ ▲ ▲
    # |1 1 1 1 1 0 0 0 0 0 0 0 0  = |         ▲ ▲ ▲ ▲ ▲
    # |1 2 1 1 2 1 0 0 0 0 0 0 0  = |        ▲ T ▲ ▲ T ▲
    # |1 1 1 1 1 1 1 0 0 0 0 0 0  = |       ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # |1 1 1 1 1 1 1 1 0 0 0 0 0  = |      ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # |1 2 1 1 2 1 1 2 1 0 0 0 0  = |     ▲ T ▲ ▲ T ▲ ▲ T ▲
    # |1 1 1 1 1 1 1 1 1 1 0 0 0  = |    ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # |1 1 2 1 1 1 1 1 1 1 1 0 0  = |   ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # |1 2 1 1 2 1 1 2 1 1 2 1 0  = |  ▲ T ▲ ▲ T ▲ ▲ T ▲ ▲ T ▲
    # |1 1 1 1 1 1 1 1 1 1 1 1 1  = | ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # o------------------------> c  o-------------------------> x
    # 1: black (▲), 2: tag (T), 0: empty

    # Define the grid
    rows = 13
    i, j = np.meshgrid(range(rows), range(rows), indexing='ij')
    grid = np.where(i + j < rows, 1, 0)
    grid[1, (1, 4, 7, 10)] = grid[4, (1, 4, 7)] = grid[7, (1, 4)] = grid[10, 1] = 2

    # Create board design instances
    # Note: when you make multiple instances of the same design, 
    #       make sure to deep copy or create new instances.
    board = BoardDesign('deltille', 'delTag25h7', grid, 10.0, 1.5)
    
    # A design can be composed of multiple board designs
    # Here we put twenty boards
    design = [copy.deepcopy(board) for i in range(20)]

    # Adjust tag id offsets to avoid overlap
    adjust_tag_id_offsets(design)

    return design
