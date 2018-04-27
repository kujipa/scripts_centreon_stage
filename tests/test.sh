source config.file

TOKEN=`$CURL -s -d "username=$USER&password=$PASSWORD" \
-X POST http://$IP_CENTREON/centreon/api/index.php?action=authenticate \
| $JQ '.["authToken"]' \
| $SED -e 's/^"//' -e 's/"$//'`

curl -s -X GET 'http://192.168.10.218/centreon/api/index.php?object=centreon_realtime_hosts&action=list' \
-H 'Content-Type: application/json' \
-H "centreon-auth-token: $TOKEN" \
| $JQ . 


