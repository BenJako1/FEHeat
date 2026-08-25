from pathlib import Path

from feheat.config import load_config
from feheat.element import create_element
from feheat.mesh import Mesh
from feheat.property import get_properties
from feheat.assembly import assemble
from feheat.boundary import load_boundary_conditions, apply_boundary_condition
from feheat.solver import steadySolver
from feheat.io import write_data

class Case:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.config = load_config(self.directory / "case.yaml")

    # Link conduction matrix generation to proper element type
    def load_element(self):
        self.element_type = self.config["element"]["type"]
        self.element = create_element(self.element_type)

    # Retrieve mesh
    def load_mesh(self):
        self.mesh = Mesh.from_msh(self.directory / self.config["mesh"], self.element_type)

    # Retrieve and apply properties
    def apply_properties(self):
        self.properties = get_properties(load_config(self.directory / self.config["properties"]))

    # Assemble
    def assemble(self):
        self.T, self.Q, self.K = assemble(self.mesh, self.element, self.properties)

    # Apply BCs
    def apply_boundary_conditions(self):
        self.boundary_conditions = load_boundary_conditions(load_config(self.directory / self.config["boundary_conditions"]))

        for bc in self.boundary_conditions:
            apply_boundary_condition(self.T, self.Q, self.K, self.mesh, self.properties, bc)
    
    # Solve
    def solve(self):
        self.T, self.Q = steadySolver.solve(self.T, self.Q, self.K, self.mesh, self.boundary_conditions)

    # Output
    def output(self):
        format = self.config["results"]["format"]
        filename = self.config["results"]["filename"]
        data = (self.mesh, self.T, self.Q)

        write_data(format, filename, data)

if __name__ == "__main__":
    pass