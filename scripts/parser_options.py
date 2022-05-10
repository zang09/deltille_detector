#!/usr/bin/python3

import argparse

from designs.get_pattern_design import name_to_design
from checkerboard import family2code as apriltag_family
from deltilleboard import family2code as deltag_family


def pattern_generator_option():
    parser = argparse.ArgumentParser(
        description="Generate a pdf with a calibration pattern."
    )
    
    # Output filename
    parser.add_argument(
        "output", nargs="?", default="pattern.pdf", help="Output pdf filename"
    )

    # Design selection
    parser.add_argument(
        "--design",
        choices=name_to_design.keys(),
        default="example_checkerboard",
        dest="design",
        help="The design name. A design is defined in designs folder. (default: %(default)s)",
    )

    # Optional tag id offset
    parser.add_argument(
        "--tag_id_offset",
        type=int,
        default=0,
        dest="tag_id_offset",
        help="Offset to bump the entire tag ids by. \
            It can be useful for generating multiple instances of a target (default: %(default)s)",
    )

    # Paper
    parser.add_argument(
        "--paper_format",
        default="a4",
        dest="paper_format",
        help="Paper format (a0, a1, ..., a5, letter, legal) (default: %(default)s)",
    )

    return parser
