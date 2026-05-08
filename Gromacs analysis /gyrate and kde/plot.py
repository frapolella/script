import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob
import re

def load_xvg(file):
    x = []
    y = []

    with open(file) as f:
        for line in f:
            if not line.startswith(('#', '@')):
                cols = line.split()
                x.append(float(cols[0]))
                y.append(float(cols[1]))

    return x, y

# searching files
pla_file = glob.glob("rgPLA*.xvg")[0]
pbat_file = glob.glob("rgPBAT*.xvg")[0]
starch_file = glob.glob("rgSTARCH*.xvg")[0]

# temperature from file name
match = re.search(r'(\d+)', pla_file)

if match:
    TEMP = match.group(1)
else:
    TEMP = "UNK"


t1, rg1 = load_xvg(pla_file)
t2, rg2 = load_xvg(pbat_file)
t3, rg3 = load_xvg(starch_file)

# plot
plt.plot(t1, rg1, label="PLA", color="red")
plt.plot(t2, rg2, label="PBAT", color="blue")
plt.plot(t3, rg3, label="Starch", color="green")

# limits
plt.xlim(0, 10000)
plt.ylim(5.8, 7.5)

# label
plt.xlabel("Time (ps)")
plt.ylabel("Rg (nm)")
plt.legend()

# saving
outfile = f"rg{TEMP}.png"

plt.savefig(outfile, dpi=300)

plt.close()

print(f"Saving plot as: {outfile}")
