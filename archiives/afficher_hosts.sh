#!/bin/bash

source config.file

TOKEN=`$CURL -s -d "username=$USER&password=$PASSWORD" \
-X POST http://$IP_CENTREON/centreon/api/index.php?action=authenticate \
| $JQ '.["authToken"]' \
| $SED -e 's/^"//' -e 's/"$//'`

## deux méthodes possibles

#curl -s -X GET 'http://$IP_CENTREON/centreon/api/index.php?object=centreon_realtime_hosts&action=list' \
#-H 'Content-Type: application/json' \
#-H "centreon-auth-token: $TOKEN" \
#| $JQ . 

curl -s -X POST "http://$IP_CENTREON/centreon/api/index.php?action=action&object=centreon_clapi" \
-H 'Content-Type: application/json' \
-H "centreon-auth-token: $TOKEN" \
--data '{ "action":"show", "object":"host"}'
