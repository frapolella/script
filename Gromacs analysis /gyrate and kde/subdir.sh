#!/bin/bash

# cartella finale dei plot
PLOTDEST="/home/francesco/Desktop/md/PLA40_200_PBAT9_68_XL_AMP60_9_trj/plot/rg"

mkdir -p "$PLOTDEST"


# gmx gyrate in subdir 

for dir in ./*/; do

    dirname=$(basename "$dir")

    # considera solo cartelle con 400/600/800
    if [[ "$dirname" =~ (400K|600K|800K) ]]; then

        echo "======================================="
        echo "$dirname"
        echo "======================================="

        cd "$dir" || continue

        # temperature
        if [[ "$dirname" =~ 400 ]]; then
            TEMP="400"
        elif [[ "$dirname" =~ 600 ]]; then
            TEMP="600"
        elif [[ "$dirname" =~ 800 ]]; then
            TEMP="800"
        fi

        # md.tpr
        if [[ ! -f "md.tpr" ]]; then
            echo "md.tpr non trovato"
            cd ..
            continue
        fi


xtcfile=$(find . -maxdepth 1 -name "*${TEMP}K*.xtc" | \
awk '
{
    match($0, /_([0-9]+)\.xtc$/, arr)
    if (arr[1] > max) {
        max = arr[1]
        file = $0
    }
}
END {
    if (file != "")
        print file
}')

if [[ -z "$xtcfile" ]]; then
    xtcfile=$(find . -maxdepth 1 -name "*${TEMP}K*.xtc" | head -1)
fi


        if [[ -z "$xtcfile" ]]; then
            echo " xtc not found"
            cd ..
            continue
        fi

        
        echo "$xtcfile"

        # gmx gyrate
        echo "PLA..."
        echo 2 | gmx gyrate -f "$xtcfile" -s md.tpr -o "rgPLA${TEMP}.xvg"

        echo "PBAT..."
        echo 3 | gmx gyrate -f "$xtcfile" -s md.tpr -o "rgPBAT${TEMP}.xvg"

        echo "STARCH..."
        echo 4 | gmx gyrate -f "$xtcfile" -s md.tpr -o "rgSTARCH${TEMP}.xvg"

        cd ..

    fi

done

# plot.py

echo "======================================="
echo " gmx gyrate completed"
echo " Starting plot.py"
echo "======================================="

for dir in */; do

    dirname=$(basename "$dir")

    if [[ "$dirname" =~ 400|600|800 ]]; then

        cd "$dir" || continue

        # temperature
        if [[ "$dirname" =~ 400 ]]; then
            TEMP="400"
        elif [[ "$dirname" =~ 600 ]]; then
            TEMP="600"
        elif [[ "$dirname" =~ 800 ]]; then
            TEMP="800"
        fi

        # plot.py
        if [[ -f "plot.py" ]]; then

            echo "Eseguo plot.py in $dirname"

            python3 plot.py

            # cp TEMP.png
            if [[ -f "rg${TEMP}.png" ]]; then

                cp "rg${TEMP}.png" "$PLOTDEST/"\
		#"$PLOTDEST/${dirname}_rg${TEMP}.png"

                echo "Copiato:"
                #echo "${dirname}_${TEMP}.png"

            else
                echo "File ${TEMP}.png not found"
            fi

        else
            echo "plot.py not found $dirname"
        fi

        cd ..

    fi

done

echo "======================================="
echo "Saving plot in:"
echo "$PLOTDEST"
echo "======================================="
