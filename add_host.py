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

# Génération d'un token
sess = requests.Session()

r = sess.post("http://{}/centreon/api/index.php?action=authenticate".format(ip),
	data={"username":"{}".format(un), "password":"{}".format(pw)})

token = r.json()['authToken']

# Fonction pour ajouter des hotes via une requete REST"""
def add_host(hostname, alias, ip, tmpl, poller, hostgroup):

	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ip),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"add", "object":"host", "values":"{};{};{};{};{};{}".format(hostname, alias, ip, tmpl, poller, hostgroup)}
		)

	if r.text == '{"result":[]}':
		print("L'hôte {} a bien été ajouté".format(hostname))

# Lecture des hotes contenus dans infohost.json
with open("infohost.json", "r") as fichier:
	contenu = fichier.read()
	t = json.loads(contenu)
	for k,v in t.items():
		hn = v.get('hostname')
		al = v.get('alias')
		ip = v.get('ip')
		hg = v.get('hostgroup')

		if v.get('tmpl')=='':
			tp = 'generic-active-host'
		else :
			tp  = v.get('tmpl')

		if v.get('poller')=='':
			pl = 'central'
		else :
			pl = v.get('poller')

		add_host(hn,al,ip,tp,pl,hg)
