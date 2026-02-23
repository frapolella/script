#extract Energy values in subdirectories + vi Eamo.txt --> cp Evalues in Eamo.txt

import os
import re

def extract_energy_value(file_path):
    """Estrae il numero che segue 'Total Potential Energy :' in e.out."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                match = re.search(r'Total Potential Energy :\s*([-+]?\d+\.\d+)\s*Kcal/mole', line)
                if match:
                    return match.group(1) + " Kcal/mole"  # Restituisce il valore con l'unità
    except Exception as e:
        print(f"Errore durante la lettura di {file_path}: {e}")
    return None

def main():
    mother_folder = os.getcwd()
    results = {}

    # Cerca nelle sottocartelle
    for subfolder in sorted(os.listdir(mother_folder)):
        subfolder_path = os.path.join(mother_folder, subfolder)
        if os.path.isdir(subfolder_path):
            file_path = os.path.join(subfolder_path, "e.out")
            if os.path.exists(file_path):
                energy_value = extract_energy_value(file_path)
                if energy_value is not None:
                    results[subfolder] = energy_value

    # Scriviamo i risultati in Eamo.txt
    output_file = os.path.join(mother_folder, "Eamo.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, (folder, energy) in enumerate(results.items(), start=1):
            f.write(f"{idx} --> {energy}\n")

    print(f"Operazione completata. File salvato in: {output_file}")

if __name__ == "__main__":
    main()
