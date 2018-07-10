#!/bin/bash

# V1.0 - 10/07/2018
# ALH 

# Script d'installation de Centreon
# A lancer sur une VM CentOS7 vierge

# Mettre à jour le système
yum -y update

# Désactiver SELinux
cd /etc/selinux/
cp config config.old
sed 's/=enforcing/=disabled/' config.old > config

# Installation du dépôt Centreon
yum -y install wget
wget http://yum.centreon.com/standard/3.4/el7/stable/noarch/RPMS/centreon-release-3.4-4.el7.centos.noarch.rpm
yum -y install --nogpgcheck centreon-release-3.4-4.el7.centos.noarch.rpm

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
systemctl stop firewalld
systemctl disable firewalld
#systemctl status firewalld

# Modification de la limitation LimitNOFILE
mkdir -p /etc/systemd/system/mariadb.service.d/
echo -ne "[Service]\nLimitNOFILE=32000\n" | tee /etc/systemd/system/mariadb.service.d/limits.conf
systemctl daemon-reload

# Lancer les ervices au démarrage 
systemctl enable httpd.service
systemctl enable snmpd.service
systemctl enable mysql.service

reboot


