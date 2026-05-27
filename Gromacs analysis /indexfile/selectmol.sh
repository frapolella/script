
for i in {1..200}
do
	mol_number=$((i - 200))
	gmx select -s md.tpr -on "pla_${mol_number}.ndx" -select "residue ${i}"
done

