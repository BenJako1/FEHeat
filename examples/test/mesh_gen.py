import gmsh
import sys

gmsh.initialize()

gmsh.model.add("mesh")

lc = 1

h = 20
r = 5

gmsh.model.occ.addCylinder(0, 0, 0, 0, h, 0, r)

gmsh.model.occ.synchronize()

volume = gmsh.model.getEntities(dim=3)

gmsh.model.addPhysicalGroup(3, [1], name="body")

gmsh.model.addPhysicalGroup(2, [1], name="wall")
gmsh.model.addPhysicalGroup(2, [2], name="top")
gmsh.model.addPhysicalGroup(2, [3], name="bottom")

gmsh.model.mesh.generate(3)

gmsh.write("mesh.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()