#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import json

sess = requests.Session()

r = sess.post('http://192.168.10.218/centreon/api/index.php?action=authenticate', 
	data={'username':'admin', 'password':'admincentreon'})

token = r.json()['authToken']

print("Veuillez entrer l'hote à supprimer :")
rep = input()

r = sess.post('http://192.168.10.218/centreon/api/index.php?action=action&object=centreon_clapi', 
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}, 
	json={"action":"del", "object":"host", "values":"{}".format(rep)}
	)

if r.text == '{"result":[]}':
	print("L'hôte {} a bien été supprimé".format(rep))




