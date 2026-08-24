from dataclasses import dataclass
import numpy as np
from feheat.utils import edge_length, tri_area, tet_volume

@dataclass
class BoundaryCondition:
    body: str
    boundary: str
    condition: str
    args: tuple

def load_boundary_conditions(data):
    boundary_conditions = []

    for body in data.keys():
        for name, bc in data[body].items():
            args = bc.get("args", ())

            if not isinstance(args, (list, tuple)):
                args = (args,)
            else:
                args = tuple(args)

            boundary_conditions.append(
                BoundaryCondition(
                    body = body,
                    boundary = name,
                    condition = bc["condition"],
                    args = args,
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
    q = bc.args[0]

    if len(bc.args) != 1:
        raise ValueError(f"Flux condition on boundary {bc.boundary} takes only one argument!")

    for face in nodes:
        type = mesh.physical_groups[bc.boundary]["type"]
        if type == "T3":
            f = q * tri_area(mesh.nodes[face]) * np.ones(3) / 3
        elif type == "L2":
            f = q * properties[bc.body]["t"] * edge_length(mesh.nodes[face]) * np.ones(2) / 2

        Q[face] += f

def apply_gen(T, Q, K, mesh, properties, bc):
    nodes = mesh.physical_groups[bc.boundary]["elements"]
    
    q = bc.args[0]

    if len(bc.args) != 1:
        raise ValueError(f"Generation condition on boundary {bc.boundary} takes only one argument!")

    for face in nodes:
        type = mesh.physical_groups[bc.boundary]["type"]
        if type == "TET4":
            f = q * tet_volume(mesh.nodes[face]) * np.ones(4) / 4
        elif type == "T3":
            f = q * properties[bc.body]["t"] * tri_area(mesh.nodes[face]) * np.ones(3) / 3
        elif type == "L2":
            f = q * properties[bc.body]["A"] * properties[bc.body]["t"] * edge_length(mesh.nodes[face]) * np.ones(2) / 2
        
        Q[face] += f

def apply_convection(T, Q, K, mesh, properties, bc):
    nodes = mesh.physical_groups[bc.boundary]["elements"]

    h, T_inf = bc.args
    
    if len(bc.args) != 2:
        raise ValueError(f"Convection condition on boundary {bc.boundary} takes two arguments!")

    for face in nodes:
        type = mesh.physical_groups[bc.boundary]["type"]
        if type == "T3":
            A = tri_area(mesh.nodes[face])
            f = h * T_inf * A * np.ones(3) / 3
            k = (h * A / 12) * np.array([[2, 1, 1],
                                         [1, 2, 1],
                                         [1, 1, 2]])
        elif type == "L2":
            A = properties[bc.body]["t"] * edge_length(mesh.nodes[face])
            f = h * T_inf * A * np.ones(2) / 2
            k = (h * A / 6) * np.array([[2, 1],
                                        [1, 2]])

        Q[face] += f
        K[np.ix_(face, face)] += k

BOUNDARY_CONDITIONS = {
    "temp": apply_temperature,
    "flux": apply_flux,
    "gen": apply_gen,
    "conv": apply_convection
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

def calculate_characteristic(type, coords):
    try:
        function = CHAR_CALC[type]
    except KeyError:
        raise ValueError(f"Unknown element type: {type!r}")
    
    return function(coords), 