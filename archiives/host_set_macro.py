#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import requests
import json

sess = requests.Session()

r = sess.post('http://192.168.10.218/centreon/api/index.php?action=authenticate', 
	data={'username':'admin', 'password':'admincentreon'})

token = r.json()['authToken']

print("Veuillez entrer l'hote à modifier :")
host = input()
print("Veuillez entrer la macro à modifier/créer :")
param = input()
print("Veuillez entrer la valeur de la macro :")
val = input()

r = sess.post('http://192.168.10.218/centreon/api/index.php?action=action&object=centreon_clapi', 
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}, 
	json={"action":"setmacro", "object":"host", "values":"{};{};{}".format(host,param,val)}
	)

if r.text == '{"result":[]}':
	print("La macro {} de l'hôte {} a bien été modifié en {}".format(param,host,val))


