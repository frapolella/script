#!/bin/bash

# Final destination folder
PLOTDEST="/home/francesco/Desktop/md/PLA40_200_PBAT9_68_XL_AMP60_9_trj/plot/hbond"

# Create destination only if missing
mkdir -p "$PLOTDEST"

###############################################
# LOOP OVER SUBDIRECTORIES
###############################################

for dir in ./*/; do

    dirname=$(basename "$dir")

    # Process only temperature folders
    if [[ "$dirname" =~ (400K|600K|800K) ]]; then

        echo "======================================="
        echo "Entering: $dirname"
        echo "======================================="

        cd "$dir" || continue

        ###############################################
        # Extract temperature
        ###############################################

        if [[ "$dirname" =~ 400 ]]; then
            TEMP="400"
        elif [[ "$dirname" =~ 600 ]]; then
            TEMP="600"
        elif [[ "$dirname" =~ 800 ]]; then
            TEMP="800"
        fi

        ###############################################
        # Check topology
        ###############################################

        if [[ ! -f "md.tpr" ]]; then
            echo "md.tpr not found"
            cd ..
            continue
        fi

        ###############################################
        # Find trajectory
        ###############################################

        xtcfile=$(find . -maxdepth 1 -name "*${TEMP}K*.xtc" | head -1)

        if [[ -z "$xtcfile" ]]; then
            echo "No xtc file found"
            cd ..
            continue
        fi

        echo "Using trajectory:"
        echo "$xtcfile"

        ###############################################
        # Create category folders
        ###############################################

        mkdir -p num
        mkdir -p dist
        mkdir -p life

        ###############################################
        # HBOND MATRIX
        ###############################################

        groups=(2 3 4)

        for i in "${groups[@]}"; do

            for j in "${groups[@]}"; do

                echo "Running H-bond: $i -> $j"

                printf "%s\n%s\n" "$i" "$j" | \
                gmx hbond \
                    -f "$xtcfile" \
                    -s md.tpr \
                    -r 0.35 \
                    -a 30 \
                    -num "num/hb_${i}_${j}_${TEMP}.xvg" \
                    -dist "dist/dist_${i}_${j}_${TEMP}.xvg" \
                    -life "life/life_${i}_${j}_${TEMP}.xvg"

            done

        done

        ###############################################
        # Copy category folders
        ###############################################

        echo "Copying folders to destination..."

        cp -r num "$PLOTDEST/${dirname}_num"
        cp -r dist "$PLOTDEST/${dirname}_dist"
        cp -r life "$PLOTDEST/${dirname}_life"

        cd ..

    fi

done

echo "======================================="
echo "HBond workflow completed!"
echo "Results copied to:"
echo "$PLOTDEST"
echo "======================================="
