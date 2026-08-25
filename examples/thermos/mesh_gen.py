import gmsh
import math
import sys

gmsh.initialize()

gmsh.model.add("mesh")

# Define dimensions
r1 = 10
r2 = 12
r3 = 15
r4 = 4
r5 = 6
t1 = 2
t2 = 2
t3 = 2
t4 = 1
h1 = 20
d1 = 8

angle = math.pi/8

lc = 0.6

p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
p2 = gmsh.model.geo.addPoint(r2, 0, 0, lc)
p3 = gmsh.model.geo.addPoint(r2, h1-t2, 0, lc)
p4 = gmsh.model.geo.addPoint(r3, h1-t2, 0, lc)
p5 = gmsh.model.geo.addPoint(r3, h1, 0, lc)
p6 = gmsh.model.geo.addPoint(r1, h1, 0, lc)
p7 = gmsh.model.geo.addPoint(r1, t1, 0, lc)
p8 = gmsh.model.geo.addPoint(0, t1, 0, lc)

l1 = gmsh.model.geo.addLine(p1, p2)
l2 = gmsh.model.geo.addLine(p2, p3)
l3 = gmsh.model.geo.addLine(p3, p4)
l4 = gmsh.model.geo.addLine(p4, p5)
l5 = gmsh.model.geo.addLine(p5, p6)
l6 = gmsh.model.geo.addLine(p6, p7)
l7 = gmsh.model.geo.addLine(p7, p8)
l8 = gmsh.model.geo.addLine(p8, p1)

loop1 = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4, l5, l6, l7, l8])
surface1 = gmsh.model.geo.addPlaneSurface([loop1], 1)

p21 = gmsh.model.geo.addPoint(0, d1, 0, lc)
p22 = gmsh.model.geo.addPoint(r5, d1, 0, lc)
p23 = gmsh.model.geo.addPoint(r5, h1, 0, lc)
p24 = p6
p25 = p5
p26 = gmsh.model.geo.addPoint(r3, h1+t3, 0, lc)
p27 = gmsh.model.geo.addPoint(r4, h1+t3, 0, lc)
p28 = gmsh.model.geo.addPoint(r4, d1+t4, 0, lc)
p29 = gmsh.model.geo.addPoint(0, d1+t4, 0, lc)

l21 = gmsh.model.geo.addLine(p21, p22)
l22 = gmsh.model.geo.addLine(p22, p23)
l23 = gmsh.model.geo.addLine(p23, p24)
l24 = gmsh.model.geo.addLine(p24, p25)
l25 = gmsh.model.geo.addLine(p25, p26)
l26 = gmsh.model.geo.addLine(p26, p27)
l27 = gmsh.model.geo.addLine(p27, p28)
l28 = gmsh.model.geo.addLine(p28, p29)
l29 = gmsh.model.geo.addLine(p29, p21)

loop2 = gmsh.model.geo.addCurveLoop([l21, l22, l23, l24, l25, l26, l27, l28, l29])
surface2 = gmsh.model.geo.addPlaneSurface([loop2], 2)

gmsh.model.geo.revolve([(2, 1), (2, 2)], 0, 0, 0, 0, 1, 0, angle, [5])

gmsh.model.addPhysicalGroup(3, [1], name="body1")
gmsh.model.addPhysicalGroup(2, [29], name="1_bottom")
gmsh.model.addPhysicalGroup(2, [33], name="1_outside")

#gmsh.model.geo.revolve([(2, 2)], 0, 0, 0, 0, 1, 0, angle, [10])

gmsh.model.addPhysicalGroup(3, [2], name="body2")
gmsh.model.addPhysicalGroup(2, [94, 91], name="2_well")

gmsh.model.geo.synchronize()

gmsh.model.mesh.generate(3)

gmsh.write("mesh.msh")

if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()
