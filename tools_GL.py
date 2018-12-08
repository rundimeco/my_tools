#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import codecs
import re
import os
import json


def moyenne(liste, s=0):
  for a in liste:s+=a
  return s/len(liste)


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
