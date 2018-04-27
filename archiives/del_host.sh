#!/bin/bash

source config.file

TOKEN=`$CURL -s -d "username=$USER&password=$PASSWORD" \
-X POST http://$IP_CENTREON/centreon/api/index.php?action=authenticate \
| $JQ '.["authToken"]' \
| $SED -e 's/^"//' -e 's/"$//'`

curl -s -X POST "http://$IP_CENTREON/centreon/api/index.php?action=action&object=centreon_clapi" \
-H 'Content-Type: application/json' \
-H "centreon-auth-token: $TOKEN" \
--data '{ "action":"del", "object":"host", "values":"test"}'
