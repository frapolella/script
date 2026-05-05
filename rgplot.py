#xvg extension Gromacs plot for 3 molecules

import matplotlib.pyplot as plt

def load_xvg(file):
    x = []
    y = []
    with open(file) as f:
        for line in f:
            if not line.startswith(('#','@')):
                cols = line.split()
                x.append(float(cols[0]))
                y.append(float(cols[1]))
    return x, y

#load_exe
t1, rg1 = load_xvg("rgPLA.xvg")
t2, rg2 = load_xvg("rgPBAT.xvg")
t3, rg3 = load_xvg("rgSTARCH.xvg")

#plot
plt.plot(t1, rg1, label="PLA", color="red")
plt.plot(t2, rg2, label="PBAT", color="blue")
plt.plot(t3, rg3, label="Starch", color="green")

#lim
plt.xlim(0, 10000)
plt.ylim(6.0, 7.3)

#label and legend
plt.xlabel("Time (ps)")
plt.ylabel("Rg (nm)")
plt.legend()
plt.show()

#savefig
#plot.savefig("rgplot.png", dpi=300)
~                                    
