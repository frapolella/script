from ase.io import read
atoms = read("mos2.cif")
atoms *= [1, 1, 1]
#print(atoms)
#print(len(atoms))
#print(atoms.get_chemical_symbols())

from BigDFT.Interop.ASEInterop import ase_to_bigdft
from BigDFT.Systems import System  #---> genera syst
from BigDFT.UnitCells import UnitCell  #---> importa unitcell
sys = System()   #----> genera sys effettivo
sys["SUR:1"] = ase_to_bigdft(atoms) #---> nome sist e da dove prende gli atomi
sys.cell = UnitCell([float(atoms.cell[0, 0]), float("inf"), float(atoms.cell[2, 2])], units="angstroem")


from BigDFT.IO import XYZReader
from BigDFT.Fragments import Fragment
with XYZReader("O2") as ifile:  #---> cerca file O2 come frag da aggiungere
    sys["ABS:2"] = Fragment(xyzfile=ifile)

sys["ABS:2"].translate([x - y for x, y in zip(sys["SUR:1"].centroid, sys["ABS:2"].centroid)]) #---> trasla
sys["ABS:2"].translate([0, 0.4*sys.cell[2, 2], 0]) #---> trasla



#viz=InlineVisualizer(400, 300) #---> attiva visualizzatore + dimensione
#viz.display_system(sys)

sys["SUR:1"].frozen = "fxyz" #----> blocca sistema e congela atomi

#INPUT
from BigDFT.Inputfiles import Inputfile
inp = Inputfile()
inp.set_xc("LDA")
inp.set_hgrid("0.5")
inp.optimize_geometry(method="SQNM", betax=1.0) #--->definisce la minimizzazione, il metodo e il passo dell'opt


from BigDFT import Calculators as C   #---> importa il calcolatore

study = C.SystemCalculator(verbose=True, omp=2, mpi_run='mpirun -np 2')
    #skip=True
log = study.run(input=inp, posinp=sys.get_posinp(), name="optslap", run_dir="optslap") # prende input e posiz sist --> crea log chiamato optslap" in cartella "optslap"
sys.update_positions_from_dict(log.log["Atomic structure"]) #---> applica dict interno


from BigDFT import Logfiles as lf
logs =lf.Logfile("optslap/log-optslap.yaml")
energy =logs.energy 
forces = logs.forcemax  #---> search forces steps

from BigDFT.Fragments import pairwise_distance
from copy import deepcopy
distance = []
systems = []
energy = []
for step in log:
    systems.append(deepcopy(sys))
    systems[-1].update_positions_from_dict(step.astruct)
    energy.append(step.energy)
    distance.append(pairwise_distance(systems[-1]["SUR:1"], systems[-1]["ABS:2"])) #---> studia le distanze dei frag


from matplotlib import pyplot as plt
fig, axs = plt.subplots(1,1)
axs.plot(energy, 'kx', label="energy")
axs.set_ylabel("Energy (Hartree)", fontsize=12)
axs2 = axs.twinx()
axs2.plot(distance, 'r+', label="Distance")
axs2.set_ylabel("Distance (Bohr)", fontsize=12)
axs.set_xlabel("Iteration", fontsize=12)
axs.legend(loc="upper center")
axs2.legend(loc="upper right")
axs.ticklabel_format(useOffset=False)
plt.savefig("plot.png", dpi=300)
