How to use the scripts

The codes opens every subdir and starts a radio of gyration analysis ---> command used = gmx gyration -f *.xtc -s md.tpr -o output.xvg
The output name is composed as rg*residue name*T.xvg ---> rg = radio of gyration; T = temperature extract from directory name
Basically gyrate.sh does:
1) Open every subdir named with a temperature(400, 600 or 800°K).
2) Starts "gmx gyration" line asking which file choose as xtc file ---> type manually
3) Start analysis of 3 residue contained in *.xtc/md.tpr
4) Initiate plot.py ---> a py script which generate the plots
5) Save plots in a chosen dir ---> remember to copy the directory path into subdir.sh or kde.sh 

kde.sh works in a similar way:
1) Looks for files with the same residue name but different temperature
2) generates kde vs rg plots via kdevsrg.py
3) Save plots in a chosen dir ---> remember to copy the directory path into subdir.sh or kde.sh 

To run the code do:

bash analysis.sh.

select which analysis is needed
