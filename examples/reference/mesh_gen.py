import gmsh
import sys

gmsh.initialize()
gmsh.model.add("mesh")

# Geometry
lc = 7  # characteristic mesh size

p1 = gmsh.model.geo.addPoint(0, 5, 0, lc)
p2 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(5, 5, 0, lc)
p4 = gmsh.model.geo.addPoint(5, 0, 0, lc)
p5 = gmsh.model.geo.addPoint(10, 5, 0, lc)
p6 = gmsh.model.geo.addPoint(10, 0, 0, lc)

# Boundary lines
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p4)
l3 = gmsh.model.geo.addLine(p4, p6)
l4 = gmsh.model.geo.addLine(p6, p5)
l5 = gmsh.model.geo.addLine(p5, p3)
l6 = gmsh.model.geo.addLine(p3, p1)

# Closed surface
loop = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4, l5, l6])
surface = gmsh.model.geo.addPlaneSurface([1])

# Synchronize geometry with the Gmsh model
gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(1, [l1], name="left")
gmsh.model.addPhysicalGroup(1, [l2, l3], name="bottom")
gmsh.model.addPhysicalGroup(1, [l4], name="right")
gmsh.model.addPhysicalGroup(1, [l5, l6], name="top")

gmsh.model.addPhysicalGroup(2, [surface], name="surface")

gmsh.option.setNumber("Mesh.Algorithm", 9)

# Generate a 2D triangular mesh
gmsh.model.mesh.generate(2)

# Save all elements
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Write the mesh
gmsh.write("mesh.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()