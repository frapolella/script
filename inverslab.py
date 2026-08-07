#!/usr/bin/env python3

"""
Correzione MoS2 con doppio piano Mo.

Input:
    B.xyz

Operazioni:
    - identifica piani Mo lungo z
    - elimina secondo piano Mo
    - mantiene tutti gli S
    - corregge distanze Mo-S
    - output B_new.xyz
"""


from pathlib import Path
import numpy as np
import sys



# ======================================================
# PARAMETRI
# ======================================================

REMOVE_PLANE = 2

TARGET_MS = 2.413

DIST_TOL = 0.03

Z_TOL = 0.05



# ======================================================
# LETTURA XYZ
# ======================================================

def read_xyz(filename):

    lines = Path(filename).read_text().splitlines()

    natoms = int(lines[0])

    atoms = []


    for line in lines[2:2+natoms]:

        p = line.split()

        atoms.append(
            (
                p[0],
                np.array(
                    [
                        float(p[1]),
                        float(p[2]),
                        float(p[3])
                    ]
                )
            )
        )


    return atoms



# ======================================================
# SCRITTURA XYZ
# ======================================================

def write_xyz(filename, atoms):

    with open(filename,"w") as f:

        f.write(
            f"{len(atoms)}\n"
        )

        f.write(
            "MoS2 corrected\n"
        )


        for s,p in atoms:

            f.write(
                f"{s:<3s}"
                f" {p[0]:15.8f}"
                f" {p[1]:15.8f}"
                f" {p[2]:15.8f}\n"
            )



# ======================================================
# DISTANZA
# ======================================================

def distance(a,b):

    return np.linalg.norm(a-b)



# ======================================================
# TROVA PIANI Mo
# ======================================================

def find_mo_planes(atoms):


    mo_indices = [

        i

        for i,(s,_)
        in enumerate(atoms)

        if s=="Mo"

    ]


    mo_indices.sort(
        key=lambda i: atoms[i][1][2]
    )


    planes=[]


    for i in mo_indices:


        z = atoms[i][1][2]


        if len(planes)==0:

            planes.append([i])

            continue



        zmean=np.mean(

            [
                atoms[j][1][2]
                for j in planes[-1]
            ]

        )



        if abs(z-zmean)<Z_TOL:

            planes[-1].append(i)

        else:

            planes.append([i])



    return planes



# ======================================================
# CORREZIONE S
# ======================================================

def correct_s_positions(atoms):


    mo_indices=[

        i

        for i,(s,_)
        in enumerate(atoms)

        if s=="Mo"

    ]


    corrected=0



    for i,(symbol,pos) in enumerate(atoms):


        if symbol!="S":

            continue



        closest=None

        minimum=999



        for mi in mo_indices:


            d=distance(

                pos,

                atoms[mi][1]

            )



            if d < minimum:

                minimum=d

                closest=mi



        if closest is None:

            continue



        if abs(minimum-TARGET_MS)<=DIST_TOL:

            continue



        mo_pos=atoms[closest][1]


        vector=pos-mo_pos


        norm=np.linalg.norm(vector)



        if norm==0:

            continue



        new_pos=(

            mo_pos

            +

            vector/norm

            *

            TARGET_MS

        )



        print(

            f"S {i}: "
            f"{minimum:.4f} Å -> "
            f"{TARGET_MS:.4f} Å"

        )


        atoms[i]=(

            "S",

            new_pos

        )


        corrected+=1



    print()

    print(
        "S corretti:",
        corrected
    )



    return atoms



# ======================================================
# MAIN
# ======================================================

def main():


    if len(sys.argv)<2:

        print(
            "Uso:"
            " python3 correct_mos2.py B.xyz"
        )

        return



    input_file=sys.argv[1]


    atoms=read_xyz(input_file)



    print("==============================")
    print("STRUTTURA INIZIALE")
    print("==============================")


    print(
        "Atomi:",
        len(atoms)
    )

    print(
        "Mo:",
        sum(s=="Mo" for s,_ in atoms)
    )

    print(
        "S:",
        sum(s=="S" for s,_ in atoms)
    )



    # --------------------------------------------------
    # trova piani Mo
    # --------------------------------------------------

    planes=find_mo_planes(atoms)



    print("\nPiani Mo trovati:")



    for n,p in enumerate(planes,1):

        print(

            f"Piano {n}: "
            f"z={np.mean([atoms[i][1][2] for i in p]):.6f} "
            f"Mo={len(p)}"

        )



    if len(planes)<REMOVE_PLANE:

        raise RuntimeError(
            "Piano da eliminare non trovato"
        )



    # --------------------------------------------------
    # rimuovi secondo piano Mo
    # --------------------------------------------------

    remove=set(

        planes[REMOVE_PLANE-1]

    )


    print()

    print(
        "Elimino piano Mo:",
        REMOVE_PLANE
    )

    print(
        "Mo eliminati:",
        len(remove)
    )



    atoms_new=[

        atom

        for i,atom
        in enumerate(atoms)

        if i not in remove

    ]



    print()

    print(
        "Dopo rimozione:"
    )


    print(
        "Atomi:",
        len(atoms_new)
    )


    print(
        "Mo:",
        sum(s=="Mo" for s,_ in atoms_new)
    )


    print(
        "S:",
        sum(s=="S" for s,_ in atoms_new)
    )



    # --------------------------------------------------
    # corregge S
    # --------------------------------------------------

    atoms_new=correct_s_positions(
        atoms_new
    )



    # --------------------------------------------------
    # output
    # --------------------------------------------------

    write_xyz(
        "B_new.xyz",
        atoms_new
    )



    print()

    print("==============================")

    print(
        "Creato B_new.xyz"
    )


    print(
        "Atomi finali:",
        len(atoms_new)
    )

    print("==============================")




if __name__=="__main__":

    main()
