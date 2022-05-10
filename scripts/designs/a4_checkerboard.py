#!/usr/bin/python3

import copy
import numpy as np

from board_design import BoardDesign, adjust_tag_id_offsets
from typing import List


def a4_checkerboard() -> List[BoardDesign]:
    """9x13 checkerboard with 8 aprilTags fit in A4, 3 pages"""
    # ↑ r                           ↑ y                          
    # |1 0 1 0 1 0 1 0 1 0 1 0 1  = | ■   ■   ■   ■   ■   ■   ■  
    # |0 1 0 1 0 1 0 1 0 1 0 1 0  = |   ■   ■   ■   ■   ■   ■    
    # |1 0 2 0 1 0 2 0 1 0 2 0 1  = | ■   T   ■   T   ■   T   ■  
    # |0 1 0 1 0 1 0 1 0 1 0 1 0  = |   ■   ■   ■   ■   ■   ■    
    # |1 0 1 0 2 0 1 0 2 0 1 0 1  = | ■   ■   T   ■   T   ■   ■  
    # |0 1 0 1 0 1 0 1 0 1 0 1 0  = |   ■   ■   ■   ■   ■   ■    
    # |1 0 2 0 1 0 2 0 1 0 2 0 1  = | ■   T   ■   T   ■   T   ■  
    # |0 1 0 1 0 1 0 1 0 1 0 1 0  = |   ■   ■   ■   ■   ■   ■    
    # |1 0 1 0 1 0 1 0 1 0 1 0 1  = | ■   ■   ■   ■   ■   ■   ■  
    # o------------------------> c  o-------------------------> x
    # 1: black (■), 2: tag (T), 0: empty
    
    # Define the grid
    rows = 9
    cols = 13
    i, j = np.meshgrid(range(rows), range(cols), indexing='ij')
    grid = np.where((i + j) % 2 == 0, 1, 0)
    grid[2, (2, 6, 10)] = grid[4, (4, 8)] = grid[6, (2, 6, 10)] = 2

    # Create board design instances
    # Note: when you make multiple instances of the same design,
    #       make sure to deep copy or create new instances.
    board = BoardDesign('checkerboard', 'aprilTag25h7', grid, 20.0)
    board2 = BoardDesign('checkerboard', 'aprilTag25h7', grid, 20.0)
    board3 = copy.deepcopy(board)

    # A design can be composed of multiple board designs
    # Here we put three boards as an example
    design = [board, board2, board3]

    # Adjust tag id offsets to avoid overlap
    adjust_tag_id_offsets(design)

    return design
