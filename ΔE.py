#for d in d do x - y = z --> ΔE

import os
import re
import numpy as np
import matplotlib.pyplot as plt

def extract_energy_value(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Trova la riga contenente "*** OPTIMIZATION RUN DONE ***"
        for i in range(len(lines)):
            if '*** OPTIMIZATION RUN DONE ***' in lines[i]:
                j = i - 1
                while j >= 0:
                    match = re.search(r'([-+]?[0-9]*\.?[0-9]+)', lines[j])
                    if match:
                        return float(match.group(0))  # Convertiamo in numero
                    j -= 1
    except Exception as e:
        print(f"Errore durante la lettura di {file_path}: {e}")
    return None

def main():
    mother_folder = os.getcwd()  
    filename_to_search = input("Inserisci il nome del file da cercare (con estensione): ").strip()
    results = {}

    for subfolder in sorted(os.listdir(mother_folder)):
        subfolder_path = os.path.join(mother_folder, subfolder)
        if os.path.isdir(subfolder_path):
            file_path = os.path.join(subfolder_path, filename_to_search)
            if os.path.exists(file_path):
                energy_value = extract_energy_value(file_path)
                if energy_value is not None:
                    results[subfolder] = energy_value

    # Scriviamo i risultati in E.txt
    output_file = os.path.join(mother_folder, "E.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for folder, energy in results.items():
            f.write(f"{folder} --> {energy}\n")

    print(f"Operazione completata. File salvato in: {output_file}")

    # Chiediamo i valori di E(PPIL), E(PP), E(IL) per ogni cartella
    deltaE_values = []
    labels = list(results.keys())  # Nomi delle cartelle
    for folder in labels:
        print(f"\nInserisci i valori per la cartella {folder}:")
        e_ppil = results[folder]  # Questo è il valore già estratto
        e_pp = float(input(f"E(PP) per {folder}: "))
        e_il = float(input(f"E(IL) per {folder}: "))
        
        deltaE = e_ppil - e_pp - e_il  # Calcolo ΔE
        deltaE_values.append(deltaE)

    # Creiamo il grafico
    plt.figure(figsize=(8, 6))
    plt.plot(labels, deltaE_values, marker='o', linestyle='-', color='b', label="ΔE")

    # Aggiungiamo etichette
    plt.xlabel("Cartelle")
    plt.ylabel("ΔE (Energy Difference)")
    plt.title("Andamento di ΔE per ogni cartella")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    # Salviamo il grafico
    graph_path = os.path.join(mother_folder, "DeltaE_graph.png")
    plt.savefig(graph_path)
    plt.show()

    print(f"Grafico salvato in: {graph_path}")

if __name__ == "__main__":
    main()
