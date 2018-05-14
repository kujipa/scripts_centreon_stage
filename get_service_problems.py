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
r = sess.get("http://{}/centreon/api/index.php?object=centreon_realtime_services&action=list&fields=id,state".format(ip),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}
		)

#pprint.pprint(r.json())

a = r.json()
i,t,w,c,u=0,0,0,0,0
l=len(a)
while i<l:
	if a[i]['state']!='0':
		t = t+1
	if a[i]['state']=='1':
		w = w+1
	if a[i]['state']=='2':
		c = c+1
	if a[i]['state']=='3':
		u = u+1

	i=i+1

print("Il y a un total de {} services".format(l))
print("Il y a {} services dans un état anormal".format(t))
print("    => {} services dans un état WARNING".format(w))
print("    => {} services dans un état CRITICAL".format(c))
print("    => {} services dans un état UNKNOWN".format(u))
