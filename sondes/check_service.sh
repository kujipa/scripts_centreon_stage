#!/bin/bash
#
# Filename - check_service
#
# Program: Checks if a service is running
# 2018 ALH 
#
# check_test v1.0 27/03/2018
#
# Description :
#
#  This plugin checks if a service is up on a Debian/Ubuntu machine
#
# Usage :
#
#  check_service -s service_name
#

set -eu

# Nagios return codes
STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3

# Plugin variable description
PROGNAME=`basename $0`
RELEASE="Revision 1.0"
AUTHOR="2018 ALH"

# Functions plugin usage
print_release() {
    echo "$RELEASE $AUTHOR"
}

print_usage() {
	echo ""
	echo "$PROGNAME $RELEASE - Service checking"
	echo ""
	echo "Usage: check_file_size.sh [ -v ] [ -h ]"
	echo ""
	echo "-s  service to check"
	echo "-h  Show this page"
	echo "-v  version"
	echo ""
	echo "Usage: $PROGNAME"
	echo "Usage: $PROGNAME --help"
	echo ""
}

print_help() {
		print_usage
        echo ""
        print_release $PROGNAME $RELEASE
        echo ""
	exit 0
}


while [ $# -gt 0 ]; do
    case "$1" in
        -h | --help)
            print_help
            exit $STATE_OK
            ;;
        -v | --version)
            print_release
            exit $STATE_OK
            ;;
        -s | --service)
            shift
            SERVICE=$1
            ;;
        *)  echo "Unknown argument: $1"
            print_usage
            exit $STATE_UNKNOWN
            ;;
        esac
shift
done


# service --status-all
# [ + ]  acpid
# [ - ]  alsa-utils
# [ - ]  anacron
# [ + ]  apparmor
# [ + ]  apport

#-----------------------------------------------------------------------------------------
# Commands
#-----------------------------------------------------------------------------------------

STATUS=`service --status-all | grep -w $SERVICE | awk '{print $2}'`

if [ $STATUS = "+" ]; then
    echo "The service $SERVICE is running"
    exit $STATE_OK
elif [ $STATUS = "-" ]; then
    echo "The service $SERVICE is inactive"
    exit $STATE_CRITICAL
else
    echo "Service inconnu"
    exit $STATE_UNKNOWN
fi


