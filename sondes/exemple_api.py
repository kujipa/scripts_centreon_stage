#Identifiants pour l'API Centreon
ipc = "192.168.66.108"
un = "admin"
pw = "centreon"

#Génération d'un token
sess = requests.Session()

r = sess.post("http://{}/centreon/api/index.php?action=authenticate".format(ipc),
	data={"username":"{}".format(un), "password":"{}".format(pw)})

token = r.json()['authToken']

#Fonction pour créer un service
def add_service_ndo(hostname, sd, tmpl):
	
	r = sess.post("http://{}/centreon/api/index.php?action=action&object=centreon_clapi".format(ipc),
		headers={"centreon-auth-token": token, 'Content-Type': 'application/json'},
		json={"action":"add", "object":"service", "values":"{};{};{}".format(hostname, sd, tmpl)}
	)

	if r.text == '{"result":[]}':
		print("Le service {} a bien été ajouté".format(sd))

#Creation d'un service
add_service_ndo("dtb_ndo_import", "synchro_ndo", "ndo_import")