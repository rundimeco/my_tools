##coding:utf-8
import justext, sys
import glob
import codecs
import re
import os

source = sys.argv[1] #répertoire où se trouvent les fichiers à scrapper
destination = re.sub("_html", "_JT", source)

if source == destination:
  print("Source and destination are the same (source name needs to contain '_html' to be replaced by '_JT'")
  exit()
liste_fic = glob.glob("%s/*"%source)

try:
  os.makedirs(destination)
except:
  print("Répertoire de destination déjà créé : %s"%destination)
language = "Portuguese"

approve = False
for cpt,fic in enumerate(liste_fic):
  if cpt%1000==0:
    print(str(cpt) + " files done")
  try:
    f = codecs.open(fic, "r", "utf-8")
    texte = f.read()
    f.close()
  except:
    continue
  newfic = re.sub("_html/", "_JT/", fic)
  if os.path.exists(newfic):
    continue
  elif len(texte)<10:
    continue
  paragraphs = justext.justext(texte, justext.get_stoplist(language))
  liste_paragraphes = []
  for paragraph in paragraphs:
    if not paragraph.is_boilerplate:
      liste_paragraphes.append(paragraph.text)
  w = codecs.open(newfic, "w", "utf-8")
  for par in liste_paragraphes:
    w.write("<p>"+par+"</p>\n")
  w.close()
  if approve ==False:
    print("Is everything OK with destination : %s ?"%destination)
    dd = raw_input("If yes, press enter, else ctrl-c")
    approve = True
