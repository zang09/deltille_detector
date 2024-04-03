#!/usr/bin/python3

import copy
import numpy as np

from board_design import BoardDesign, adjust_tag_id_offsets
from typing import List

def a4_deltille() -> List[BoardDesign]:
    """9x11 deltille board with 10 deltags fit in A4, 3 pages"""
    # ↑ r                                     ↑ y           ↗ r 
    # |0 0 0 0 1 1 1 1 1 1 1 1 1 1 0  = |    ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ 
    # |0 0 0 1 1 2 1 1 2 1 1 2 1 1 0  = |   ▲ ▲ T ▲ ▲ T ▲ ▲ T ▲ ▲  
    # |0 0 0 1 1 1 1 1 1 1 1 1 1 0 0  = |    ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ 
    # |0 0 1 1 1 1 1 1 1 1 1 1 1 0 0  = |   ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
    # |0 0 1 1 1 2 1 1 2 1 1 1 0 0 0  = |    ▲ ▲ ▲ T ▲ ▲ T ▲ ▲ ▲ 
    # |0 1 1 1 1 1 1 1 1 1 1 1 0 0 0  = |   ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
    # |0 1 1 1 1 1 1 1 1 1 1 0 0 0 0  = |    ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ 
    # |1 1 2 1 1 2 1 1 2 1 1 0 0 0 0  = |   ▲ ▲ T ▲ ▲ T ▲ ▲ T ▲ ▲  
    # |1 1 1 1 1 1 1 1 1 1 0 0 0 0 0  = |    ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
    # o-------------------------------> c  o----------------------> x
    # 1: black (▲), 2: tag (T), 0: empty
    
    # Define the grid
    rows = 9
    cols = 10
    i, j = np.meshgrid(range(rows), range(cols + (rows + 1)//2), indexing='ij')
    grid = np.where((j >= (rows - i - 1)//2) & (j < (rows - i)//2 + cols), 1, 0)    
    grid[1, 5] = grid[1, 8] = grid[1, 11] = \
    grid[4, 5] = grid[4, 8] = \
    grid[7, 2] = grid[7, 5] = grid[7, 8] = 2
    
    # Create board design instances
    # Note: when you make multiple instances of the same design, 
    #       make sure to deep copy or create new instances.
    board = BoardDesign('deltille', 'delTag25h7', grid, 25.0)
    board2 = BoardDesign('deltille', 'delTag25h7', grid, 25.0)
    board3 = copy.deepcopy(board)
    
    # A design can be composed of multiple board designs
    # Here we put three boards as an example
    design = [board, board2, board3]

    # Adjust tag id offsets to avoid overlap
    adjust_tag_id_offsets(design)

    return design
