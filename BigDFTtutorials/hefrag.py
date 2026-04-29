from BigDFT.Atoms import Atom
at1 = Atom({'r': [1.0, 0.0, 0.0], 'sym':"He", 'units':'bohr', "nzion": 2})
at2 = Atom({'r': [3.0, 0.0, 0.0], 'sym':"He", 'units':'bohr', "nzion": 2})

from BigDFT.Fragments import Fragment
frag = Fragment()
frag.append(at1)
frag.append(at2)


for at in frag:
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
