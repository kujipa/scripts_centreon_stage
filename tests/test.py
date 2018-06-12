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



r = sess.post('http://192.168.10.91/centreon/api/index.php?action=action&object=centreon_clapi', 
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'}, 
	json={"action":"setparam", "object":"contact", "values":"t_alias;svcnotifperiod;workhours"}
	)


print(r.text)


