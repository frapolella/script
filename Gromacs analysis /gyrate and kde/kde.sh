#!/bin/bash

PLOTDEST="/home/francesco/Desktop/md/PLA40_200_PBAT9_68_XL_AMP60_9_trj/plot/kdevsrg"

mkdir -p "$PLOTDEST"

# remove temporary files
rm -f rgPLA*.xvg
rm -f rgPBAT*.xvg
rm -f rgSTARCH*.xvg


# cp files in subdir 


for dir in ./*/; do

    dirname=$(basename "$dir")

    if [[ "$dirname" =~ (400|600|800) ]]; then

        echo "Reading $dirname"

        find "$dir" -maxdepth 1 -name "rgPLA*.xvg" -exec cp {} . \;
        find "$dir" -maxdepth 1 -name "rgPBAT*.xvg" -exec cp {} . \;
        find "$dir" -maxdepth 1 -name "rgSTARCH*.xvg" -exec cp {} . \;

    fi

done


#Python launcher


python3 kdevsrg.py


# cp png


cp kdevsrgPLA.png "$PLOTDEST/"
cp kdevsrgPBAT.png "$PLOTDEST/"
cp kdevsrgSTARCH.png "$PLOTDEST/"

echo "Plot saved in:"
echo "$PLOTDEST"

