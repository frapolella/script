#!/bin/bash
cp *.xtc aglc/
cp md.tpr aglc/
#cp topol.top
cd aglc/
mkdir -p rg

TPR="md.tpr"

XTC=$(ls *.xtc | head -n1)

if [[ -z "$XTC" ]]; then
    echo "No xtc file found"
    exit 1
fi

echo "Using trajectory: $XTC"

for i in $(seq 1 9)
do

    NDX="aglc${i}.ndx"
    OUT="rg/aglc${i}.xvg"

    if [[ ! -f "$NDX" ]]; then
        echo "Missing $NDX"
        continue
    fi

    echo "Running $NDX"

    printf "5\n" | gmx gyrate \
        -f "$XTC" \
        -s "$TPR" \
        -n "$NDX" \
	#-b 1 -e 500 \
        -o "$OUT"

done

mv *.xvg rg/

echo "Completed"
