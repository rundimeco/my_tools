import re
import sys
import json
from tools_GL import *

if len(sys.argv)!=3:
  print("USAGE : argv1=csv_file argv2=out_name")

lignes = open_utf8(sys.argv[1], True )

path_out = sys.argv[2]
entetes = re.split(";", re.sub("\n","",lignes[0]))

liste_out = []
for lig in lignes[1:]:
  dic = {}
  elems = re.split(";", re.sub("\n","",lig))
  for i, nom in enumerate(entetes):
    dic[nom] = elems[i]
  liste_out.append(dic)
write_utf8(path_out, json.dumps(liste_out))
