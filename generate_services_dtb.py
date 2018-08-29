#!/usr/bin/env python2.7
# -*- coding: utf8 -*-
#
# 1) Récupère la liste des DTB (nom, IP) depuis la base ODEM
# 2) Génère des fichiers de services pour nagios (services_ping_dtb.cfg, services_dtb_ndo.cfg)
#
# À mettre en crontab journalière avec reload de nagios
# Nécessite un client oracle + python cx_Oracle + export LD_LIBRARY_PATH="/usr/lib/oracle/12.1/client/lib"
#

import sys
import argparse
import cx_Oracle as oracle

import requests
import json
import pprint
import json

#Identifiants pour l'API Centreon
ipc = "192.168.66.108"
un = "admin"
pw = "centreon"

parser = argparse.ArgumentParser()
parser.add_argument('--blacklist_ping', action='append')
parser.add_argument('--override', action='append')

parsed = parser.parse_args(sys.argv[1:])

#Recuperer la liste des DTB
dtbs_request = '''
select  lgl_ctr.name as contrat,
        ci_dtb.DTB_NAME as DTB_NAME,
        ( select SRV_IP from ODEM.ci_server where srv_id = ci_dtb.SRV_ID ) as dtb_ip
from    ODEM.CI_DTB ci_dtb,
        ODEM.CI ci,
        ODEM.ENV_CI,
        ODEM.CURRENT_LEGAL_CONTRACT lgl_ctr
where   ci.CI_ID = ci_dtb.CI_ID
and     ( ci.CI_ENDDATE is null or ci.CI_ENDDATE > sysdate )
and     env_ci.CI_ID = ci_dtb.CI_ID
and     env_ci.LGL_CTR_ID = lgl_ctr.LGL_CTR_ID
and     ( lgl_ctr.DATE_RESILIATION is null or  lgl_ctr.DATE_RESILIATION > sysdate )
and     DTB_JDBCNDO is not null
'''

odem_user = "digora"
odem_passwd = "dig5918"
odem_tns = "ODEM"

con = oracle.connect(odem_user + "/" + odem_passwd + "@" + odem_tns)
cur = con.cursor()

cur.execute(dtbs_request)
dtbs = cur.fetchall()


#Token
sess = requests.Session()

r = sess.post("http://{}/centreon/api/index.php?action=authenticate".format(ipc),
	data={"username":"{}".format(un), "password":"{}".format(pw)})

token = r.json()['authToken']


def add_host(hostname, alias, iph, tmpl, poller, hostgroup):

	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"add", "object":"host", "values":"{};{};{};{};{};{}".format(hostname, alias, iph, tmpl, poller, hostgroup)}
		)

	if r.text == '{"result":[]}':
		print("L'hote {} a bien ete ajoute".format(hostname))
		
		
def del_host(hostname):

	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"del", "object":"host", "values":"{}".format(hostname)}
		)

	if r.text == '{"result":[]}':
		print("L'hote {} a bien ete supprime".format(hostname))
		
		
def add_service_ndo(hostname, sd, tmpl, dtb_name):
	
	#Creation du service
	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"add", "object":"service", "values":"{};{};{}".format(hostname, sd, tmpl)}
	)

	if r.text == '{"result":[]}':
		print("Le service {} a bien ete ajoute".format(sd))

	#Arguments pour la commande
	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"setparam", "object":"service", "values":"{};{};check_command_arguments;!ndo!{}!15".format(hostname, sd, dtb_name)}
	)
	if r.text == '{"result":[]}':
		print("Le service {} a bien ete modifie".format(dtb_name))


def add_service_ping(hostname, sd, tmpl, dtb_name, dtb_ip):
	
	#Creation du service
	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"add", "object":"service", "values":"{};{};{}".format(hostname, sd, tmpl)}
	)

	if r.text == '{"result":[]}':
		print("Le service {} a bien ete ajoute".format(sd))

	#Arguments pour la commande
	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"setparam", "object":"service", "values":"{};{};check_command_arguments;!{}!500,10%!1000,20%!1".format(hostname, sd, dtb_ip)}
	)
	if r.text == '{"result":[]}':
		print("Le service {} a bien ete modifie".format(dtb_name))

				
#Suppression et ajout des hotes
del_host("dtb_ndo_import")
del_host("dtb_ping")
add_host("dtb_ndo_import", "dtb_ndo_import", "192.168.66.250", "generic-server-host", "Central", "ZALL")
add_host("dtb_ping", "dtb_ping", "192.168.66.250", "generic-server-host", "Central", "ZALL")

#Alternative
#os.system('/usr/share/centreon/bin/centreon -u admin -p centreon -o HOST -a ADD -v "test6;test_6;126.0.0.1;generic-active-host;central;"')
  
for dtb in dtbs:
	contract, dtb_name, dtb_ip = dtb
	print(dtb_name)
	
	#Service description
	sdndo = "NDO import " + dtb_name
	sdping = "Ping DTB " + dtb_name
	
	#Ajout du service pour toutes les DTB
	add_service_ndo("dtb_ndo_import", sdndo, "ndo_import", dtb_name)
	add_service_ping("dtb_ping", sdping, "ping_hwcp", dtb_name, dtb_ip)
	
#Application de la configuration
r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
	headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
	json={"values": "central","action":"applycfg"})

pprint.pprint(r.json())


print('Finished!')
