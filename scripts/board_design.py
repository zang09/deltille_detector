#!/usr/bin/python3

import numpy as np
from typing import List

class BoardDesign:
    """Class to store single board specification

    Args:
        board_type (str): Board type; "checkerboard" or "deltille"
        tag_family (str): Tag family
        grid (np.ndarray): Grid matrix
        size (float): The size (i.e. edge length) of base polygon [mm]
        tag_border (float): Tag border thickness. Ratio to one bit size
    """
    def __init__(self,
                 board_type: str,
                 tag_family: str,
                 grid: np.ndarray,
                 size: float,
                 tag_border: float = 2.0,
                 tag_id_offset: int = 0,
                 ):
        self.board_type = board_type
        self.tag_family = tag_family
        self.grid = grid
        self.size = size
        self.tag_border = tag_border
        self.tag_id_offset = tag_id_offset


def adjust_tag_id_offsets(design: List[BoardDesign]):
    """Go over the input design and adjust tag id offsets so that no tag
    in the same family overlaps between boards

    Args:
        design (List[BoardDesign]): A list of board designs that will be updated
    """
    num_tags_in_family = {}
    
    for board in design:
        num_tags = np.count_nonzero(board.grid == 2)
        
        if board.tag_family not in num_tags_in_family:
            # no offset for the first board in the family
            board.tag_id_offset = 0
            num_tags_in_family[board.tag_family] = num_tags
        else:
            # otherwise, assign the offset
            board.tag_id_offset = num_tags_in_family[board.tag_family]
            num_tags_in_family[board.tag_family] += num_tags
