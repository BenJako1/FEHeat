import meshio
from pathlib import Path
import os
import numpy as np

def write_vtu(filename, data):
    if not os.path.exists("results"):
        os.mkdir("results")

    filepath = f"results/{filename}.vtu"

    mesh, T, Q = data

    points = mesh.nodes

    MESHIO_CELL_TYPES = {
        "T3": "triangle",
        "TET4": "tetra"
    }

    cells = [(MESHIO_CELL_TYPES[mesh.element_type], mesh.elements)]

    point_data = {"Temperature": T}

    meshio.write_points_cells(filepath, points, cells, point_data=point_data)

FORMATS = {
    "vtu": write_vtu
}

def write_data(format, filename, data):
    try:
        write_function = FORMATS[format]
    except:
        raise ValueError(f"Unknown file format: {format}."
                         f"Available types: {list(FORMATS)}")

    return write_function(filename, data)