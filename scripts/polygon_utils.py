#!/usr/bin/python3

import math

from pyx import canvas, path, unit
from shapely.geometry import Polygon


def round7(x):
    # round floating-point at precision 7 to help polygon processing
    return round(x, 7)


def polygon_square(x, y, width):
    # return  a square polygon at (x, y)
    return Polygon(
        [
            [round7(x), round7(y)],
            [round7(x + width), round7(y)],
            [round7(x + width), round7(y + width)],
            [round7(x), round7(y + width)],
        ]
    )


def polygon_triangle60(x, y, width):
    # return an inverted triangle of which the bottom corner is at (x, y)
    c60 = 0.5
    s60 = math.sqrt(3.0) / 2
    return Polygon(
        [
            [round7(x), round7(y)],
            [round7(x + width * c60), round7(y + width * s60)],
            [round7(x - width * c60), round7(y + width * s60)],
        ]
    )


def polygon_triangle(x, y, width):
    # return a triangle of which the bottom-left corner is at (x, y)
    c60 = 0.5
    s60 = math.sqrt(3.0) / 2
    return Polygon(
        [
            [round7(x), round7(y)],
            [round7(x + width), round7(y)],
            [round7(x + width * c60), round7(y + width * s60)],
        ]
    )


def draw_polygons(c: canvas.canvas, polygons, fillColor, holeColor=None):
    # assuming polygons is either "Polygon" or "MultiPolygon"
    if polygons.geom_type == "Polygon":
        polylist = [polygons]
    else:
        polylist = polygons.geoms

    for poly in polylist:
        # draw exterior
        coords = list(poly.exterior.coords)
        if coords:
            ppath = path.path(
                path.moveto_pt(
                    unit.topt(coords[0][0]), unit.topt(coords[0][1]))
            )
            for i in range(1, len(coords)):
                ppath.append(
                    path.lineto_pt(
                        unit.topt(coords[i][0]), unit.topt(coords[i][1]))
                )
            ppath.append(
                path.lineto_pt(
                    unit.topt(coords[0][0]), unit.topt(coords[0][1]))
            )
            ppath.append(path.closepath())
            c.fill(ppath, [fillColor])
        else:
            print("Warning: polygon is empty.")

        # draw interior (there might be multiple)
        if holeColor is not None:
            for interior in poly.interiors:
                coords = list(interior.coords)
                if coords:
                    ppath = path.path(
                        path.moveto_pt(
                            unit.topt(coords[0][0]), unit.topt(coords[0][1]))
                    )
                    for i in range(1, len(coords)):
                        ppath.append(
                            path.lineto_pt(
                                unit.topt(coords[i][0]), unit.topt(
                                    coords[i][1])
                            )
                        )
                    ppath.append(
                        path.lineto_pt(
                            unit.topt(coords[0][0]), unit.topt(coords[0][1]))
                    )
                    ppath.append(path.closepath())
                    c.fill(ppath, [holeColor])
