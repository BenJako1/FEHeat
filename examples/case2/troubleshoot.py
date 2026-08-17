import meshio

mesh = meshio.read("mesh.msh")

for i, cell_block in enumerate(mesh.cells):
    print(
        i,
        cell_block.type,
        cell_block.data.shape
    )

print(mesh.cell_data.keys())

for name, data in mesh.cell_data.items():
    print(name, len(data))

#meshio.write("mesh.vtu", mesh)