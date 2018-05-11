#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import json
import pprint

# Info de configuration
with open("configfile.json", "r") as fichier:
	contenu = fichier.read()
	t = json.loads(contenu)
	ip = t['IP_CENTREON']
	un = t['USER']
	pw = t['PASSWORD']


# génération du token
sess = requests.Session()

r = sess.post("http://{}/centreon/api/index.php?action=authenticate".format(ip),
	data={"username":"{}".format(un), "password":"{}".format(pw)})

token = r.json()['authToken']


# affichage du status des hosts
r = sess.get("http://{}/centreon/api/index.php?object=centreon_realtime_services&action=list".format(ip),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}
		)

pprint.pprint(r.json())
