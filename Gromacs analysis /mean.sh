#this code do:
#1) Search 8 file called aglc
#2) Extract the second column. Using awk ignores any line containing letters
#3) Generate a all column file via paste
#4) Does sum and mean for all column via akw (row1 + row2 +row3)/NF

ifiles=()

for i in {1..8}; do
    [[ -f "aglc${i}.xvg" ]] && files+=( "aglc${i}.xvg" )
done

nfiles=${#files[@]}

if [[ $nfiles -eq 0 ]]; then
    echo "No aglc*.xvg files found"
    exit 1
fi

echo "Found $nfiles files"

#processa colnne

for f in "${files[@]}"; do

    echo "Processing $f"
    base=$(basename "$f" .xvg)
    awk '$1 ~/^[0-9]/ {print $2}' "$f" >> "${base}presum"
done

paste *presum > needsumtmp
# Row sum
LC_NUMERIC=C awk '
{
        sum= 0.0 
        for(i=1;i<=NF;i++){
               sum += $i + 0.0
       }
       printf "%.5f\n", sum/NF 
}' needsumtmp > meantmp
