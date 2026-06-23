#!/bin/bash
#cd aglc/rg/
files=()

for i in {1..9}; do
    [[ -f "aglc${i}.xvg" ]] && files+=( "aglc${i}.xvg" )
done

nfiles=${#files[@]}

if [[ $nfiles -eq 0 ]]; then
    echo "No aglc*.xvg files found"
    exit 1
fi

echo "Found $nfiles files"

for f in "${files[@]}"
do
    echo "Processing $f"

    base=$(basename "$f" .xvg)

    awk '$1~/^[0-9]/ {print $2}' "$f" \
    > "${base}presum"

done

paste *presum > needsumtmp

LC_NUMERIC=C awk '
{
sum=0
for(i=1;i<=NF;i++)
sum+=$i

printf "%.5f\n",sum/NF
}' needsumtmp > meantmp.xvg

echo "Created meantmp.xvg"
