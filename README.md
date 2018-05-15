# Instructions pour l'utilisation des scripts

## Ajout d'hotes
__Script__ : *add_host.py*

La liste des hôtes à ajouter doit être renseignée dans le fichier *list_info_host.json*
en respectant la structure

Seules les valeurs hostname, alias, ip sont obligatoires



## Afficher les élèments
__Script__ : *show.py*

Permet d'afficher la liste d'une catégorie d'objet (hôtes, services, ...)

La liste des possibilités est disponible en tapant -h ou --help à la suite du script



## Execution d'une suite d'instructions
__Script__ : *super_script.py*

Permet d'exécuter une suite d'instructions écrites dans le fichier *instructions.txt*

L'historique des commandes exécutées est stocké dans *log_instructions*



## Afficher tous les hôtes en détails
__Script__ : *get_host_status.py*

Permet d'afficher la liste détaillée des hosts



## Afficher tous les services en détails
__Script__ : *get_service_status.py*

Permet d'afficher la liste détaillée des services



## Afficher le nombre d'hôtes dans un état anormal
__Script__ : *get_host_problems.py*

Permet d'afficher le détail des hosts dans un état anormal 



## Afficher le nombre de services dans un état anormal
__Script__ : *get_service_problems.py*

Permet d'afficher le détail des services dans un état anormal 



## Appliquer les changements 
__Script__ : *applycfg.py*

Permet la prise en compte des changements par Centreon



## Autres
__Fichier__ : *configfile.json*

Contient les infos de connexion au serveur Centreon

__Fichier__ : *parametres_host.txt*

Contient tous les paramètres modifiables sur un host

__Fichier__ : *instructions.txt*

Contient une suite d'instructions => une instruction par ligne, format OBJET ACTION PARAMETRES
Ligne débute par *#* => ligne de commentaire, ne sera pas executé 

