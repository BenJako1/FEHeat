import numpy as np

class steadySolver:
    def solve(T, Q, K, mesh, bcs):
        K_sol = K.copy()
        Q = Q.copy()

        boundNodes = []

        for bc in bcs:
            if bc.condition == 'temp':
                boundNodes += mesh.physical_groups[bc.boundary]["elements"].tolist()

        boundNodes = np.sort(np.unique(boundNodes))
        freeNodes = np.array([int(i) for i in range(mesh.N) if i not in boundNodes])

        # remove rows
        for count, bn in enumerate(boundNodes):
            K = np.delete(K, bn - count, axis=0)
            Q = np.delete(Q, bn - count, axis=0)

        # subtract known boundary temperatures
        for bn in boundNodes:
            Q -= K[:, bn] * T[bn]

        # remove columns
        for count, bn in enumerate(boundNodes):
            K = np.delete(K, bn - count, axis=1)

        T_unknown = np.linalg.solve(K, Q)

        Tsol = np.zeros(mesh.N)
        for i, fn in enumerate(freeNodes):
            Tsol[fn] = T_unknown[i]
        for bn in boundNodes:
            Tsol[bn] = T[bn]

        Qsol = K_sol @ Tsol

        if round(np.sum(Qsol), 5) != 0:
            raise ValueError("Flux is non-conservative!")
    
        return Tsol, Qsol