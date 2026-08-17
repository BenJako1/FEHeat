import gmsh
import sys

gmsh.initialize()
gmsh.model.add("mesh")

l = 10
w = 2
h = 1

# Geometry
lc = 0.3  # characteristic mesh size

p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(l, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(l, w, 0, lc)
p4 = gmsh.model.geo.addPoint(0, w, 0, lc)

p5 = gmsh.model.geo.addPoint(0, 0, h, lc)
p6 = gmsh.model.geo.addPoint(l, 0, h, lc)
p7 = gmsh.model.geo.addPoint(l, w, h, lc)
p8 = gmsh.model.geo.addPoint(0, w, h, lc)

# Boundary lines
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)

l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p5)

l9 = gmsh.model.geo.addLine(p1, p5)
l10 = gmsh.model.geo.addLine(p2, p6)
l11 = gmsh.model.geo.addLine(p3, p7)
l12 = gmsh.model.geo.addLine(p4, p8)

# Closed surface
loop1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
surface1 = gmsh.model.geo.addPlaneSurface([loop1])

loop2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
surface2 = gmsh.model.geo.addPlaneSurface([loop2])

loop3 = gmsh.model.geo.addCurveLoop([l1, l10, -l5, -l9])
surface3 = gmsh.model.geo.addPlaneSurface([loop3])

loop4 = gmsh.model.geo.addCurveLoop([l2, l11, -l6, -l10])
surface4 = gmsh.model.geo.addPlaneSurface([loop4])

loop5 = gmsh.model.geo.addCurveLoop([l3, l12, -l7, -l11])
surface5 = gmsh.model.geo.addPlaneSurface([loop5])

loop6 = gmsh.model.geo.addCurveLoop([l4, l9, -l8, -l12])
surface6 = gmsh.model.geo.addPlaneSurface([loop6])

surface_loop = gmsh.model.geo.addSurfaceLoop([surface1, surface2, surface3, surface4, surface5, surface6])
volume = gmsh.model.geo.addVolume([surface_loop])

# Synchronize geometry with the Gmsh model
gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(2, [surface1], name="z_minus")
gmsh.model.addPhysicalGroup(2, [surface2], name="z_plus")
gmsh.model.addPhysicalGroup(2, [surface3], name="y_minus")
gmsh.model.addPhysicalGroup(2, [surface4], name="x_plus")
gmsh.model.addPhysicalGroup(2, [surface5], name="y_plus")
gmsh.model.addPhysicalGroup(2, [surface6], name="x_minus")

gmsh.model.addPhysicalGroup(3, [volume], name="body")

# Generate a 3D tetrahedral mesh
gmsh.model.mesh.generate(3)

# Save all elements
#gmsh.option.setNumber("Mesh.SaveAll", 1)

# Write the mesh
gmsh.write("mesh.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()