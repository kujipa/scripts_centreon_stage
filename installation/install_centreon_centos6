#!/bin/bash

# V1.0 - 10/07/2018
# ALH 

# Script d'installation de Centreon
# A lancer sur une VM CentOS6 vierge

# Mettre à jour le système
yum -y update

# Désactiver SELinux
cd /etc/selinux/
cp config config.old
sed 's/=enforcing/=disabled/' config.old > config

# Installation du dépôt Centreon
yum -y install wget
wget http://yum.centreon.com/standard/3.4/el6/stable/noarch/RPMS/centreon-release-3.4-4.el6.noarch.rpm
yum -y install --nogpgcheck centreon-release-3.4-4.el6.noarch.rpm

# Installation d’un serveur central 
yum -y install centreon-base-config-centreon-engine centreon

# Installer de la base de données sur le central : 
yum -y install MariaDB-server
service mysql restart

# php timezone
touch /etc/php.d/php-timezone.ini
echo "date.timezone = Europe/Paris" | tee -a /etc/php.d/php-timezone.ini
systemctl restart httpd

# Desactive le pare-feu
/etc/init.d/iptables save
/etc/init.d/iptables stop
chkconfig iptables off

# Lancer les ervices au démarrage 
chkconfig httpd on
chkconfig snmpd on
chkconfig mysql on

reboot

