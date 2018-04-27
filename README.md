# Instructions pour l'utilisation des scripts

## Ajout d'hotes
__Script__ : _add_host.py_
La liste des hôtes à ajouter doit être renseignée dans le fichier _infohost.json_
en respectant la structure
Seules les valeurs hostname, alias, ip sont obligatoires


## Afficher les élèments
__Script__ : _show.py_
Permet d'afficher la liste d'une catégorie d'objet (hôtes, services, ...)
La liste des possibilités est disponible en tapant -h ou --help à la suite du script


## Execution d'une suite d'instructions
__Script__ : _super_script.py_
Permet d'exécuter une suite d'instructions écrites dans le fichier _instructions.txt_
L'historique des commandes exécutées est stocké dans _log_instructions_


## Autres
__Fichier__ : _configfile.json_
Contient les infos de connexion au serveur Centreon
__Fichier__ : _parametres_host.txt_
Contient tous les paramètres modifiables sur un host
