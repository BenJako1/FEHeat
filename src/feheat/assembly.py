import numpy as np

def assemble(mesh, element, properties):
    # Initialise global conduction matrix
    K = np.zeros((mesh.N, mesh.N))

    # Initialize global load and temperature vectors
    Q = np.zeros(mesh.N)
    T = np.zeros(mesh.N)

    for body in properties.keys():
        elements = mesh.physical_groups[body]["elements"]
        body_properties = properties[body]
        for nodes in elements:
            Ke = element.get_K(body_properties, mesh.nodes[nodes])

            K[np.ix_(nodes, nodes)] += Ke

    return T, Q, K