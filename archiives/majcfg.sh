#!/bin/bash
# majcfc.sh
# version 1.00
# date 24/04/2018
# mettre à jour la configuration Centreon si des changements ont été appliqués via l'API

source config.file

TOKEN=`$CURL -s -d "username=$USER&password=$PASSWORD" \
-X POST http://$IP_CENTREON/centreon/api/index.php?action=authenticate \
| $JQ '.["authToken"]' \
| $SED -e 's/^"//' -e 's/"$//'`

curl -s 'http://$IP_CENTREON/centreon/api/index.php?action=action&object=centreon_clapi' \
-H 'Content-Type: application/json' \
-H "centreon-auth-token: $TOKEN " \
--data '{"action":"applycfg", "values":"central"}'
