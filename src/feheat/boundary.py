from dataclasses import dataclass
import numpy as np
from feheat.utils import edge_length, tri_area, tet_volume

@dataclass
class BoundaryCondition:
    boundary: str
    condition: str
    args: tuple

def load_boundary_conditions(data):
    boundary_conditions = []

    for name, bc in data.items():
        args = bc.get("args", ())

        if not isinstance(args, (list, tuple)):
            args = (args,)
        else:
            args = tuple(args)

        boundary_conditions.append(
            BoundaryCondition(
                boundary=name,
                condition=bc["condition"],
                args=args,
            )
        )

    return boundary_conditions

def apply_temperature(T, Q, K, mesh, properties, bc):
    nodes = mesh.physical_groups[bc.boundary]["elements"]

    if len(bc.args) != 1:
        raise ValueError(f"Temperature condition on boundary {bc.boundary} takes only one argument!")

    T[nodes] = bc.args[0]

def apply_flux(T, Q, K, mesh, properties, bc):
    nodes = mesh.physical_groups[bc.boundary]["elements"]

    if len(bc.args) != 1:
        raise ValueError(f"Flux condition on boundary {bc.boundary} takes only one argument!")

    for face in nodes:
        type = mesh.physical_groups[bc.boundary]["type"]
        if type == "T3":
            coefficient = np.ones(3) * tri_area(mesh.nodes[face]) / 3
        elif type == "L2":
            coefficient = np.ones(2) * properties["t"] * edge_length(mesh.nodes[face]) / 2
        Q[nodes] += bc.args[0] * coefficient

BOUNDARY_CONDITIONS = {
    "temp": apply_temperature,
    "flux": apply_flux
}

def apply_boundary_condition(T, Q, K, mesh, properties, bc):
    try:
        function = BOUNDARY_CONDITIONS[bc.condition]
    except KeyError:
        raise ValueError(f"Unknown boundary condition: {bc.condition!r}")
    
    return function(T, Q, K, mesh, properties, bc)

CHAR_CALC = {
    "L2": edge_length,
    "T3": tri_area,
    "TET4": tet_volume
}

def calculate_characteristic(type, coords, properties):
    try:
        function = CHAR_CALC[type]
    except KeyError:
        raise ValueError(f"Unknown element type: {type!r}")
    
    return function(coords), 