#The script extract rg column from a gyrate xvg file

ifiles=()

for i in {1..200}; do
    [[ -f "pla${i}.xvg" ]] && files+=( "pla${i}.xvg" )
done

nfiles=${#files[@]}

if [[ $nfiles -eq 0 ]]; then
    echo "No pla*.xvg files found"
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
