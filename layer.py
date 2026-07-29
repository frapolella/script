from ase.io import read, write
from ase import Atoms
import numpy as np

atoms = read("device_MoS2_ordered.gen")
print("Original atoms:", len(atoms))

# Regions

cont1 = atoms[1040:1248].copy()
layer6   = atoms[520:624].copy()
cont2 = atoms[1248:1456].copy()
#Info regions
print("Cont1 :", len(cont1))
print("Layer6   :", len(layer6))
print("Cont2 :", len(cont2))

# Atom gap and region extention
gap = 1.592   # Å gap between atom slices

xmin_c1 = cont1.positions[:,0].min()
xmax_c1 = cont1.positions[:,0].max()

xmin_l6 = layer6.positions[:,0].min()
xmax_l6 = layer6.positions[:,0].max()

xmin_c2 = cont2.positions[:,0].min()
xmax_c2 = cont2.positions[:,0].max()


# move layer6
dx_layer = (xmax_c1 + gap) - xmin_l6
layer6.translate([dx_layer,0,0])

# move cont2
xmin_l6_new = layer6.positions[:,0].min()
xmax_l6_new = layer6.positions[:,0].max()

dx_cont2 = (xmax_l6_new + gap) - xmin_c2
cont2.translate([dx_cont2,0,0])

# merging device
new_device = cont1 + layer6 + cont2


# new periodic cell

xmin = new_device.positions[:,0].min()
xmax = new_device.positions[:,0].max()

cell = new_device.cell.copy()

cell[0,0] = (xmax - xmin) + 5.0

new_device.set_cell(cell)

new_device.set_pbc([True,True,True])


# Saving process

write("device_layer6.gen", new_device)
write("device_layer6.xyz", new_device)

print()
print("Reduced device created")
print("Atoms :", len(new_device))
print("New cell :", new_device.cell)
                                                                  
