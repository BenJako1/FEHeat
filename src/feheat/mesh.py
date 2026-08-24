import gmsh
import numpy as np

class Mesh:
    def __init__(self, nodes, elements, physical_groups, element_type):
        self.nodes = nodes
        self.elements = elements
        self.physical_groups = physical_groups

        self.element_type = element_type

        self.N = len(self.nodes)

    @classmethod
    def from_msh(cls, filepath, element_type_name):
        """
        Read a Gmsh .msh file and return nodal coordinates and
        element connectivity.

        Parameters
        ----------
        filepath : str
            Path to the Gmsh .msh file.

        Returns
        -------
        nodes : np.ndarray, shape (N, 3)
            Nodal coordinates [x, y, z].

        elements : np.ndarray, shape (nE, 3)
            Element connectivity. Each row contains the
            node indices corresponding to one element.
        """

        gmsh.initialize()

        try:
            gmsh.open(str(filepath))

            # Get all nodes
            node_tags, node_coords, _ = gmsh.model.mesh.getNodes()

            # Reshape flat coordinate array into N x 3
            nodes = np.array(node_coords, dtype=float).reshape(-1, 3)

            max_tag = int(node_tags.max())
            tag_to_index = np.full(max_tag + 1, -1, dtype=int)
            tag_to_index[node_tags] = np.arange(len(node_tags))

            # Convert legible type ("T3") to gmsh type (2)
            gmsh_type = ELEMENT_TYPES[element_type_name]

            # Search only for elements of that type
            gmsh_element_tags, node_tags = gmsh.model.mesh.getElementsByType(gmsh_type)

            _, _, _, num_nodes, _, _ = gmsh.model.mesh.getElementProperties(gmsh_type)

            elements = np.array(node_tags, dtype=np.int64).reshape(-1, num_nodes)

            physical_groups = {}
            
            dimTags = gmsh.model.getPhysicalGroups()

            for dim, physical_group in dimTags:
                entities = gmsh.model.getEntitiesForPhysicalGroup(dim, physical_group)
                name = gmsh.model.getPhysicalName(dim, physical_group)

                physical_groups[name] = {
                    "type": [],
                    "elements": []
                }

                for entity in entities:
                    element_type, element_tags, node_tags_for_entity = gmsh.model.mesh.getElements(dim, entity)
                    physical_groups[name]["type"] = INV_ELMENT_TYPES[element_type[0]]
                    _, _, _, num_nodes, _, _ = gmsh.model.mesh.getElementProperties(element_type[0])
                    group_elements = np.array(node_tags_for_entity, dtype=np.int64).reshape(-1, num_nodes)

                    physical_groups[name]["elements"] = tag_to_index[group_elements]

            # This is a shitty fix
            elements = tag_to_index[elements]

            return cls(nodes, elements, physical_groups, element_type_name)

        finally:
            gmsh.finalize()

ELEMENT_TYPES = {
    "L2": 1,
    "T3": 2,
    "TET4": 4
}

INV_ELMENT_TYPES = {v: k for k, v in ELEMENT_TYPES.items()}


if __name__ == "__main__":
    mesh = Mesh.from_msh("mesh.msh", "T3")
    print(mesh.physical_groups)