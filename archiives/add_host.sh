#!/bin/bash
#
# Filename - add_host.sh
#
# Program: Add a host on Centreon based on the infomations written in hote.file
# 2018 ALH 
#
# add_host v1.0 19/04/2018
#
# Description :
#
#  ....
#
# Usage :
#
#  ....
#

set -xeu

source hote.file
source config.file

TOKEN=`$CURL -s -d "username=$USER&password=$PASSWORD" \
-X POST http://$IP_CENTREON/centreon/api/index.php?action=authenticate \
| $JQ '.["authToken"]' \
| $SED -e 's/^"//' -e 's/"$//'`

PARAM="'{\"action\":\"add\", \"object\":\"host\", \"values\":\"$Name;$Alias;$IPAdd;$HTemp;$Poller;\"}'"
echo "$PARAM"

curl -s 'http://192.168.10.218/centreon/api/index.php?action=action&object=centreon_clapi' \
-H 'Content-Type: application/json' \
-H "centreon-auth-token: $TOKEN" \
--data "$PARAM"
#--data '{"action":"add", "object":"host", "values":"test9;Test hos9t;139.0.0.1;generic-active-host;central;"}'
#--data ${PARAM} => '{"action":"add", "object":"host", "values":"Test3;Test host;133.0.0.1;generic-active-host;central;machines_test"}'

