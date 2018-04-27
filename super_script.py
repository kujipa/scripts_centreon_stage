#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import json

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


# connaitre le nombre de lignes
f1 = open("instructions.txt","r")
nbrl = 0
for line in f1:
	nbrl += 1
f1.close()


# structure switch
def yksi():
	return('{}'.format(values[0]))

def kaksi():
	return('{};{}'.format(values[0],values[1]))

def kolme():
	return('{};{};{}'.format(values[0],values[1],values[2]))

options = { 1 : yksi , 2 : kaksi , 3 : kolme }


# stockage de l'historique des commandes
log = open("log_instructions","a")

g = open("instructions.txt","r")
i = 0
while i < nbrl:
	b = g.readline()
	log.write(b)
	c = b.split()
	objet = c[0]
	action = c[1]
	values = c[2:]

	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ip),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"{}".format(action), "object":"{}".format(objet), "values": options[len(values)]() }
		)

	print(r.text)
	i += 1

g.close()
log.close()
