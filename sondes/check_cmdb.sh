#!/bin/bash

set -eu


#hostname
hostname=$(hostname -s | sed 's/;//g')

#fqdn
fqdn=$(hostname -f | sed 's/;//g')

#os_type
os_type=Linux

if [ -r /etc/oracle-release ]
	then
  		os_version=$(cat /etc/oracle-release | sed 's/;//g')

elif [ -r /etc/centos-release ]
	then
  		os_version=$(cat /etc/centos-release | sed 's/;//g')

elif [ -r /etc/redhat-release ]
	then
  		os_version=$(cat /etc/redhat-release | sed 's/;//g')

elif [ -r /etc/debian_version ]
	then
 		 os_version=$(cat /etc/debian_version | sed 's/;//g')

else
  os_version=Unknown
fi

# manufacturer et model
if ! type dmidecode > /dev/null 2>&1
	then
  		manufacturer=Unknown
 		model=Unknown
else
  	manufacturer=$(dmidecode -t1 | grep "Manufacturer" | awk -F: '{print $2}' | sed 's/^ //g' | sed 's/;//g')
  	model=$(dmidecode -t1 | grep 'Product Name' | awk -F: '{print $2}' | sed 's/^ //g' | sed 's/;//g')
fi

#adresse ip
ipadd=""
type ifconfig 1>/dev/null 2>/dev/null
# si ifconfig existe
if [ $? -eq 0 ]
	then res=`ifconfig | grep -E "inet[ ]" | wc -l`
	
	if [ $res = 2 ]
		then 
			ipadd=`ifconfig | grep -E "inet[ ]" | awk '/inet addr:/{print $2}' | awk -F ':' '{print $2}' | sed '/127.0.0.1/d'`
	fi
#sinon on utilise ip a
else
	res=`ip a | grep -E "inet[ ]" | wc -l`

	if [ $res = 2 ]
		then 
			ipadd=`ip a | grep -E "inet[ ]" | awk '/inet /{print $2}' | sed '/127.0.0.1/d' | awk -F '/' '{print $1}'`
	fi

fi

#architecture
architecture=$(uname -i)

#resultat
echo "hostname=$hostname!!fqdn=$fqdn!!ip=$ipadd!!os_type=$os_type!!os_version=$os_version!!architecture=$architecture!!manufacturer=$manufacturer!!model=$model"
exit 0

