#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import json

# Info de configuration
with open("configfile2.json", "r") as fichier:
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


# connaitre le nombre de lignes
f1 = open("instructions.txt","r")
nbrl = 0
for line in f1:
	nbrl += 1
f1.close()


# stockage de l'historique des commandes et execution des instructions
log = open("log_instructions","a")
g = open("instructions.txt","r")
i = 0

while i < nbrl:
	b = g.readline()
	if b[0] != '#':    # si la ligne n'est pas un commentaire
		log.write(b)
		c = b.split()
		objet = c[0]
		action = c[1]
		values = c[2]
		print(values)

		r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ip),
			headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
			json={"action":"{}".format(action), "object":"{}".format(objet), "values":"{}".format(values) }
			)

		print(r.text)

	i += 1

g.close()
log.close()
