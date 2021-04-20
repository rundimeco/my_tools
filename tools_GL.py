#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import codecs
import re
import os
import json
from htmldate import find_date
def get_date(date_str):
  dic_mois = months = {"Jan":"01", "Feb":"02", "Fév":"02", "Mar":"03", "Apri":"04", "Apr":"04", "Avr":"04", "Avri":"04", "May":"05", "Mai":"05", "June":"06", "Juin":"06", "July":"07", "Juil":"07", "Aug":"08", "Aoû":"08", "Augu":"08", "Août":"0_", "Sep":"09", "Sept":"09", "Oct":"10", "Octo":"10", "Nov":"11", "Nove":"11", "Dec":"12", "Déc":12, "Inco":"00"} 
 #  date_format1 = find_date(date_str)
  date_format_fr = re.findall("([0-9]{1,2}) ([A-Za-z][a-zéû]*) ([0-9]{4})", date_str)
  if len(date_format_fr)>0:
    date_format2 = date_format_fr[0]
    annee = date_format2[2]
    mois_str  = date_format2[1]
    jour  = date_format2[0]
  else:
    date_format_en = re.findall("([A-Za-z][a-zéû]*) ([0-9]{1,2}), ([0-9]{4})", date_str)
    if len(date_format_en)>0:
      date_format2 = date_format_en[0]
      annee = date_format2[2]
      mois_str  = date_format2[0]
      jour  = date_format2[1]
    else:
    #  try:
     #   annee = re.findall(" [12][0-9]{3} ", date_str)[0]##too noisy
      #except:
      w = open("log_date.txt", "a")
      w.write(date_str[:30]+"\n")
      w.close()
      annee = "0000"
      mois_str, jour = "inconnu", "00" 
  for variante in [mois_str[:3].capitalize(), mois_str[:4].capitalize()]:
    if variante in dic_mois:
      mois_int = dic_mois[variante]
      break
    else:
      mois_int="01"#TODO correct this
  if len(jour)==1:
    jour = "0"+jour
  try:
    date_format2 = f"{annee}-{mois_int}-{jour}"
  except:
    print(date_str)
    1/0
  return date_format2

def decouper_mots(texte):
  mots = re.findall("[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ-]*", texte)
  return mots

def napalm(chaine):
  chaine = chaine.strip()
  chaine = re.sub(r'[^\w\s]','',chaine)
  chaine = re.sub(' ','_',chaine)
  return chaine

def mkdirs(path, verbose = False):
  try:
    os.makedirs(path)
  except:
    if verbose==True:
      print("%s already exists"%path)
    pass

def variance(tableau):
    m=moyenne(tableau)
    return moyenne([(x-m)**2 for x in tableau])

def ecartype(tableau):
  tableau = [float(x) for x in tableau]
  return variance(tableau)**0.5

def moyenne(liste, s=0):
  ###Function example: getting mean from a list of numbers
  for a in liste:s+=a
  return s/len(liste)

def effectif_from_list(liste):
  ###Getting items with their absolute frequency
  dic = {}
  for elem in liste:
    dic.setdefault(elem, 0)
    dic[elem]+=1
  return dic

def open_utf8(path,lines=False):
  ###Showing usage of codecs (useful for utf-8)
  f = codecs.open(path,'r','utf-8')
  if  lines==True:
    out = f.readlines()
    out = [re.sub("\n|\r","",x) for x in out]
  else:
    out = f.read()
  f.close()
  return out

def get_filename(chaine):
  elems =re.split("/",chaine)
  return elems[len(elems)-1]

def write_utf8(path, out, verbose =True, is_json = False):
  ### Writing in a file
  w = codecs.open(path,'w','utf-8')
  if is_json==False:
    w.write(out)
  else:
    w.write(json.dumps(out, indent=2, ensure_ascii=False))
  w.close()
  if verbose:
    print("Output written in '%s'"%path)

def tag_sentence(sent):
  ###Very simple tree tagger wrapper, the cmd variable needs to be adapted
  prep_sent = re.sub("\n|'|\"|-", " ", sent)
  cmd = "echo '%s' | ../external_tools/tree-tagger/cmd/tree-tagger-french >toto.tag"%prep_sent
  os.system(cmd)
  f = open("toto.tag")
  lignes = f.readlines()
  f.close()
  results = [re.split("\t", re.sub("\n","",x)) for x in lignes]
  return results

def load_json(path):
  f = open(path)
  struct = json.load(f)
  f.close()
  return struct

def do_we_force(out_name):
  ### Example usage of input for controlling overwriting of existing files
  if os.path.exists(out_name):
    q = "Output name (%s) already exists, should we process anyway ?"%out_name
    msg = input(q)
    if msg == "y" or msg =="yes":
      return True
    else:
      return False 
  else:
    return True
