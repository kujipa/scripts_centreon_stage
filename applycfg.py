#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import pprint
import sys
import json

# Info de configuration
with open("configfile2.json", "r") as fichier:
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


# Par défaut le poller est "central", mais possible de mettre un poller en argument 
try:
	poller = sys.argv[1]
except:
	poller="central"


# Application de la configuration - prises en compte des changements
r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ip),
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
	json={"values": "{}".format(poller),"action":"applycfg"})

pprint.pprint(r.json())
