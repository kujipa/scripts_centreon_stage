#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import pprint
import sys
import json

# Info de configuration
with open("configfile.json", "r") as fichier:
	contenu = fichier.read()
	t = json.loads(contenu)
	ip = t['IP_CENTREON']
	un = t['USER']
	pw = t['PASSWORD']


# Génération d'un token
sess = requests.Session()

r = sess.post("http://{}/centreon/api/index.php?action=authenticate".format(ip),
	data={"username":"{}".format(un), "password":"{}".format(pw)})

token = r.json()['authToken']


# Affichage de la liste des possibilités
if sys.argv[1] == "-h" or sys.argv[1] == "--help":
	print("Choix possibles : ACLACTION;ACLGROUP;ACLMENU;ACLRESOURCE;CENTBROKERCFG;CGICFG;CMD;CONTACT;CONTACTTTPL")
	print("CG;DEP;DOWNTIME;HTPL;HC;HG;HOST;INSTANCE;STPL;SERVICE;SG;SC;TIMEPERIOD;TRAP;VENDOR")
	print("Entrez votre choix")
	objet = input()

# Sinon on recupère l'objet demandé
else:
	objet=sys.argv[1] 

r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ip),
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
	json={"object":"{}".format(objet),"action":"show"})

pprint.pprint(r.json())
