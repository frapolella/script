import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import glob

def load_xvg(file):

    data = []

    with open(file) as f:
        for line in f:
            if not line.startswith(('#','@')):
                cols = line.split()
                data.append(float(cols[1]))

    return np.array(data)

########################################
# FUNZIONE KDE
########################################

def make_kde(residue):

    file400 = glob.glob(f"rg{residue}400.xvg")[0]
    file600 = glob.glob(f"rg{residue}600.xvg")[0]
    file800 = glob.glob(f"rg{residue}800.xvg")[0]

    rg400 = load_xvg(file400)
    rg600 = load_xvg(file600)
    rg800 = load_xvg(file800)

    kde400 = gaussian_kde(rg400)
    kde600 = gaussian_kde(rg600)
    kde800 = gaussian_kde(rg800)

    xmin = min(rg400.min(), rg600.min(), rg800.min())
    xmax = max(rg400.max(), rg600.max(), rg800.max())

    x = np.linspace(xmin, xmax, 1000)

    plt.figure()

    plt.plot(x, kde400(x), label="400K", color="red")
    plt.plot(x, kde600(x), label="600K", color="blue")
    plt.plot(x, kde800(x), label="800K", color="green")

    plt.xlabel("Rg (nm)")
    plt.ylabel("Density")
    plt.title(f"KDE vs Rg — {residue}")

    plt.legend()

    outfile = f"kdevsrg{residue}.png"

    plt.savefig(outfile, dpi=300)

    plt.close()

    print(f"Saved: {outfile}")

########################################
# GENERA TUTTI I GRAFICI
########################################

make_kde("PLA")
make_kde("PBAT")
make_kde("STARCH")
