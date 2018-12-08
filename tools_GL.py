#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import codecs
import re
import os
import json

def lcs(S,T):
  m = len(S)
  n = len(T)
  counter = [[0]*(n+1) for x in range(m+1)]
  longest = 0
  lcs_set = set()
  for i in range(m):
    for j in range(n):
      if S[i] == T[j]:
        c = counter[i][j] + 1
        counter[i+1][j+1] = c
        if c > longest:
          lcs_set = set()
          longest = c
          lcs_set.add(S[i-c+1:i+1])
        elif c == longest:
          lcs_set.add(S[i-c+1:i+1])
  if len(lcs_set)==0:
    return [""]
  return list(lcs_set)

def moyenne(liste, s=0):
  for a in liste:s+=a
  return s/len(liste)

def get_arff(dic):
  chaine = "@RELATION %s\n\n"%dic["relation"]
  sort_features = sorted(dic["features"])
  cpt_feat = 0
  for s in sort_features:
    val = dic["features"][s]#prevoir numeric
    name = "%s_"%str(cpt_feat)
    cpt_feat+=1
    for e in val:
      name+=str(e)
    name=re.sub(" ","_",name)
    if dic["numeric"]==False:typ = "{%s}"%",".join(val)
    else:typ = "NUMERIC"
    chaine+="@ATTRIBUTE %s %s\n"%(str(name),typ)
  classes = "@ATTRIBUTE class {%s}\n"%",".join(dic["classes"])
  chaine+=classes
  chaine+="\n@DATA\n"
  for instance in dic["instances"]:
    if dic["sparse"]==True:
      chaine+="{%s}\n"%",".join(instance)
    else:
      chaine+="%s\n"%",".join(instance)
  return chaine

def effectif_from_list(liste):
  dic = {}
  for elem in liste:
    dic.setdefault(elem, 0)
    dic[elem]+=1
  return dic

def open_utf8(path,l=False):
  f = codecs.open(path,'r','utf-8')
  if  l==True:
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
  w = codecs.open(path,'w','utf-8')
  if is_json==False:
    w.write(out)
  else:
    w.write(json.dumps(out, indent=2))
  w.close()
  if verbose:
    print("Output written in '%s'"%path)

def tag_sentence(sent):
  ##Tree tagger wrapper
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
  if os.path.exists(out_name):
    q = "Output name (%s) already exists, should we process anyway ?"%out_name
    msg = input(q)
    if msg == "y" or msg =="yes":
      return True
    else:
      return False 
  else:
    return True
