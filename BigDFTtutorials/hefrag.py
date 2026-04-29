from BigDFT.Atoms import Atom   #---> callss Atom to generate a small He cluster
at1 = Atom({'r': [1.0, 0.0, 0.0], 'sym':"He", 'units':'bohr', "nzion": 2}) #---> at1 = Atom({'r': [x, y, z], atsymbol, measure units, electron number})
at2 = Atom({'r': [3.0, 0.0, 0.0], 'sym':"He", 'units':'bohr', "nzion": 2})

from BigDFT.Fragments import Fragment #---> call Fragment
frag = Fragment() #---> generates a fragment ---> all atom in a fragment may display same color
frag.append(at1) #---> appeend at1 and at2 to the fragment
frag.append(at2)


for at in frag: #---> prints at in fragment
  print(dict(at))

  print(frag.centroid)
  print(frag.nel)

  from copy import deepcopy
  frag2 = deepcopy(frag)
  frag2.translate(vec=[0.0,5.0, 0.0])
  frag2.rotate(x=90, units="degrees")

  from BigDFT.Fragments import distance
  print(distance(frag, frag2))
  
  from yaml import dump
  print(dump(frag2))
