import numpy as np
from feheat.utils import *

class T3:
    def B_matrix(self, coords):
        A = tri_area(coords)
        x = coords[:, 0]
        y = coords[:, 1]
        return 1/(2*A)*np.array([[y[1]-y[2], y[2]-y[0], y[0]-y[1]],
                                   [x[2]-x[1], x[0]-x[2], x[1]-x[0]]])

    def get_K(self, properties, coords):
        k = properties["k"]
        A = tri_area(coords)
        t = properties["t"]
        B = self.B_matrix(coords)
        return k * t * A * (B.T @ B)

class TET4:
    def B_matrix(self, coords):
        A = np.concatenate((np.ones((4,1)), coords), axis=1)
        Ainv = np.linalg.inv(A)
        B = Ainv[..., 1:, :]
        return B

    def get_K(self, properties, coords):
        k = properties["k"]
        V = tet_volume(coords)
        B = self.B_matrix(coords)
        return k * V * (B.T @ B)

ELEMENT_TYPES = {
    "T3": T3,
    "TET4": TET4
}

def create_element(type):
    try:
        element_class = ELEMENT_TYPES[type]

    except KeyError:
        raise ValueError(
            f"Unknown element type: {type}. "
            f"Available types: {list(ELEMENT_TYPES)}"
            )

    return element_class()