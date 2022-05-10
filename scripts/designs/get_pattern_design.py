#!/usr/bin/python3

import sys

from designs.a4_checkerboard import a4_checkerboard
from designs.a4_deltille import a4_deltille
from designs.ico_deltille import ico_deltille
from designs.design_your_own import design_your_own

name_to_design = {
    "a4_checkerboard": a4_checkerboard,
    "a4_deltille": a4_deltille,
    "ico_deltille": ico_deltille,
    "design_your_own": design_your_own,
}


def get_pattern_design(name):
    if name not in name_to_design:
        print("[ERROR] Unknown design name")
        sys.exit(0)
        
    return name_to_design[name]()
