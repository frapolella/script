#This script runs all other *.sh and *.py script in this directory

#!/bin/bash

BASE=$(pwd)
PROC="$BASE"

dirs=(
../stat_npt_400K_14
../stat_npt_600K_11_da_10
../stat_npt_800K_08_da_06
)

for dir in "${dirs[@]}"
do
    echo "=========================="
    echo "Processing: $dir"
    echo "=========================="

    cd "$dir" || continue

    echo "--- Step 1: generate index"
    bash "$PROC/genemanu.sh"

    echo "--- Step 2: calculate gyration"
    bash "$PROC/rg_manual.sh"
done

dors=(
../stat_npt_400K_14/aglc/rg
../stat_npt_600K_11_da_10/aglc/rg
../stat_npt_800K_08_da_06/aglc/rg
)

for dor in "${dors[@]}"
do
    echo "=========================="
    echo "Processing: $dor"
    echo "=========================="

    cd "$dor" || continue

    echo "--- Step 3: process mean"   
    bash "$PROC/t.sh"

    echo "--- Step 4: create plot"
    python3 "$PROC/plotmean.py"

    cd "$BASE"

done

echo "ALL DONE"
