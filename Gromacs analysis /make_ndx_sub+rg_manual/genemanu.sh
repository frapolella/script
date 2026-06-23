#!/bin/bash

mkdir -p aglc
cd aglc || exit 1

start=111901
natoms=1263
nmol=9

for ((n=1; n<=nmol; n++))
do
    end=$((start + natoms - 1))

    echo "Generazione aglc${n}.ndx : atomi ${start}-${end}"

    printf "a %d-%d\nq\n" "$start" "$end" | \
    gmx make_ndx \
        -f ../md.tpr \
        -o aglc${n}.ndx

    start=$((end + 1))

done

echo "Completato"
