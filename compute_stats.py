import sys
sys.path.append("/home/rundimeco/Documents/code/my_tools")
import tools_GL as mt
import glob
import re

liste_docs = glob.glob(sys.argv[1]+"/*")

dic_stats = {	 
		"tab_car":[],
		"tab_par":[],
		"tot_car":0,
		"tot_par":0,
		"moy_car":0,
		"moy_par":0,
		"std_car":0,
		"std_par":0
	}

dic_stats["nb_docs"] = len(liste_docs)
for doc in liste_docs:
  f = open(doc)
  texte = f.read()
  f.close()
  lignes = re.split("\n", texte)
  clean_txt = re.sub("<p>|</p>","",texte)
  dic_stats["tab_car"].append(len(clean_txt))
  dic_stats["tab_par"].append(len(lignes))
  dic_stats["tot_car"]+=len(clean_txt)
  dic_stats["tot_par"]+=len(lignes)

dic_stats["moy_car"] = mt.moyenne(dic_stats["tab_car"])
dic_stats["moy_par"] = mt.moyenne(dic_stats["tab_par"])
dic_stats["std_car"] = mt.ecartype(dic_stats["tab_car"])
dic_stats["std_par"] = mt.ecartype(dic_stats["tab_par"])

print("Documents :"+str(dic_stats["nb_docs"]))
for cle in ["tot_car",  
"moy_car", 
"std_car", 
"tot_par", 
"moy_par", 
"std_par"]:
  print(cle, dic_stats[cle])
