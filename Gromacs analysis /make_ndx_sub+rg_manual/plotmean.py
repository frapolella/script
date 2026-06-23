import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import re

def load_xvg(file):
    x = []
    y = []
    time = 0

    with open(file) as f:
        for line in f:
            if not line.startswith(('#', '@')):
                cols = line.split()
                if cols:
                 x.append(time)
                 y.append(float(cols[0]))
                 time += 10

    return x, y

# trova automaticamente i file
#pla_file = glob.glob("rgPLA*.xvg")[0]
#pbat_file = glob.glob("rgPBAT*.xvg")[0]
starch_file = glob.glob("meantmp.xvg")[0]

# estrai temperatura dal nome file
#match = re.search(r'(\d+)', pla_file)

#if match:
#    TEMP = match.group(1)
#else:
#    TEMP = "UNK"

# carica dati
#t1, rg1 = load_xvg(pla_file)
#t2, rg2 = load_xvg(pbat_file)
t3, rg3 = load_xvg(starch_file)

# plot
#plt.plot(t1, rg1, label="PLA", color="red")
#plt.plot(t2, rg2, label="PBAT", color="blue")
plt.plot(t3, rg3, label="Starch", color="green")

# limiti
plt.xlim(0, 10000)
plt.ylim(0, 10)

# label
plt.xlabel("Time (ps)")
plt.ylabel("Rg (nm)")
plt.legend()

# salva senza mostrare
outfile = f"rg1.png" #outfile = f"rg{TEMP}.png"

plt.savefig(outfile, dpi=300)

# chiudi figura
plt.close()

print(f"Plot salvato come: {outfile}")
