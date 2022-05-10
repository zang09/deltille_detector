#!/usr/bin/python3

import os
import sys
import numpy as np

from pyx import canvas, document, unit
from checkerboard import AprilCheckerBoard
from deltilleboard import DeltilleBoard
from parser_options import pattern_generator_option
from designs.get_pattern_design import get_pattern_design

if __name__ == "__main__":
    # Setup the argument list
    parser = pattern_generator_option()
    parsed = parser.parse_args()

    # Paper formats
    pf = {
        "a0": document.paperformat.A0,
        "a0b": document.paperformat.A0b,
        "a1": document.paperformat.A1,
        "a2": document.paperformat.A2,
        "a3": document.paperformat.A3,
        "a4": document.paperformat.A4,
        "a5": document.paperformat.A5,
        "letter": document.paperformat.Letter,
        "legal": document.paperformat.Legal,
    }
    paper_format = pf[parsed.paper_format]

    # Get a design
    design = get_pattern_design(parsed.design)

    # Set default unit
    unit.set(defaultunit="mm")

    # Create a page for each board
    pages = []
    target_dsc = ""
    for board_id, board_design in enumerate(design):
        if board_design.board_type == 'checkerboard':
            board = AprilCheckerBoard(board_id, board_design, parsed.tag_id_offset)
        elif board_design.board_type == 'deltille':
            board = DeltilleBoard(board_id, board_design, parsed.tag_id_offset)

        # Draw the board in a fresh canvas
        c = canvas.canvas()
        board.draw_to_canvas(c)
        board_dsc = board.get_description()
        target_dsc += board_dsc
        
        # Convert to a page
        p = document.page(c, paperformat=paper_format,
                          rotated=1, centered=1, fittosize=0)
        pages.append(p)

    doc = document.document(pages)
    doc.writePDFfile(parsed.output)

    # Write a dsc file
    with open(os.path.splitext(parsed.output)[0] + ".dsc", "w") as f:
        f.write(target_dsc)
