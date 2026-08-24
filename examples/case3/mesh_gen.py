import gmsh
import sys

gmsh.initialize()

gmsh.model.add("mesh")

l = 10
w = 10
h1 = 10
h2 = h1 + 10

lc = 2

# Add points

p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(l, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(l, w, 0, lc)
p4 = gmsh.model.geo.addPoint(0, w, 0, lc)

p5 = gmsh.model.geo.addPoint(0, 0, h1, lc)
p6 = gmsh.model.geo.addPoint(l, 0, h1, lc)
p7 = gmsh.model.geo.addPoint(l, w, h1, lc)
p8 = gmsh.model.geo.addPoint(0, w, h1, lc)

p9 = gmsh.model.geo.addPoint(0, 0, h2, lc)
p10 = gmsh.model.geo.addPoint(l, 0, h2, lc)
p11 = gmsh.model.geo.addPoint(l, w, h2, lc)
p12 = gmsh.model.geo.addPoint(0, w, h2, lc)

# Add lines

# Bottom
l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p1)
# Mid
l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p5)
# Bottom vert
l9 = gmsh.model.geo.addLine(p1, p5)
l10 = gmsh.model.geo.addLine(p2, p6)
l11 = gmsh.model.geo.addLine(p3, p7)
l12 = gmsh.model.geo.addLine(p4, p8)
# Top
l13 = gmsh.model.geo.addLine(p9, p10)
l14 = gmsh.model.geo.addLine(p10, p11)
l15 = gmsh.model.geo.addLine(p11, p12)
l16 = gmsh.model.geo.addLine(p12, p9)
# Top vert
l17 = gmsh.model.geo.addLine(p5, p9)
l18 = gmsh.model.geo.addLine(p6, p10)
l19 = gmsh.model.geo.addLine(p7, p11)
l20 = gmsh.model.geo.addLine(p8, p12)

# Add Surfaces

# Bottom
loop1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
surface1 = gmsh.model.geo.addPlaneSurface([loop1])
# Mid
loop2 = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])
surface2 = gmsh.model.geo.addPlaneSurface([loop2])
# B front
loop3 = gmsh.model.geo.addCurveLoop([l1, l10, -l5, -l9])
surface3 = gmsh.model.geo.addPlaneSurface([loop3])
# B right
loop4 = gmsh.model.geo.addCurveLoop([l2, l11, -l6, -l10])
surface4 = gmsh.model.geo.addPlaneSurface([loop4])
# B back
loop5 = gmsh.model.geo.addCurveLoop([l3, l12, -l7, -l11])
surface5 = gmsh.model.geo.addPlaneSurface([loop5])
# B left
loop6 = gmsh.model.geo.addCurveLoop([l4, l9, -l8, -l12])
surface6 = gmsh.model.geo.addPlaneSurface([loop6])
# Top
loop7 = gmsh.model.geo.addCurveLoop([l13, l14, l15, l16])
surface7 = gmsh.model.geo.addPlaneSurface([loop7])
# T front
loop8 = gmsh.model.geo.addCurveLoop([l5, l18, -l13, -l17])
surface8 = gmsh.model.geo.addPlaneSurface([loop8])
# T right
loop9 = gmsh.model.geo.addCurveLoop([l6, l19, -l14, -l18])
surface9 = gmsh.model.geo.addPlaneSurface([loop9])
# T back
loop10 = gmsh.model.geo.addCurveLoop([l7, l20, -l15, -l19])
surface10 = gmsh.model.geo.addPlaneSurface([loop10])
# T left
loop11 = gmsh.model.geo.addCurveLoop([l8, l17, -l16, -l20])
surface11 = gmsh.model.geo.addPlaneSurface([loop11])

surface_loop1 = gmsh.model.geo.addSurfaceLoop([surface1, surface2, surface3, surface4, surface5, surface6])
body1 = gmsh.model.geo.addVolume([surface_loop1])

surface_loop2 = gmsh.model.geo.addSurfaceLoop([surface2, surface7, surface8, surface9, surface10, surface11])
body2 = gmsh.model.geo.addVolume([surface_loop2])

gmsh.model.geo.synchronize()

gmsh.model.addPhysicalGroup(2, [surface1], name="z_minus")
gmsh.model.addPhysicalGroup(2, [surface7], name="z_plus")
gmsh.model.addPhysicalGroup(2, [surface3], name="y_minus")
gmsh.model.addPhysicalGroup(2, [surface4], name="x_plus")
gmsh.model.addPhysicalGroup(2, [surface5], name="y_plus")
gmsh.model.addPhysicalGroup(2, [surface6], name="x_minus")

gmsh.model.addPhysicalGroup(3, [body1], name="body1")
gmsh.model.addPhysicalGroup(3, [body2], name="body2")

gmsh.model.mesh.generate(3)

gmsh.write("mesh.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()