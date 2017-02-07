#!/bin/bash

#
# Set hostname and networking
#
echo "%NAME%.dendory.net" > /etc/hostname
chattr +i /etc/hostname
echo "search dendory.net" > /etc/resolv.conf
echo "domain dendory.net" >> /etc/resolv.conf
echo "nameserver 8.8.8.8" >> /etc/resolv.conf
chattr +i /etc/resolv.conf
echo "preserve_hostname: true" >> /etc/cloud/cloud.cfg

#
# Disable SELinux
#
systemctl restart network
echo "SELINUX=disabled" > /etc/selinux/config
echo "SELINUXTYPE=targeted" >> /etc/selinux/config
setenforce 0

#
# Install EPEL and missing packages
#
yum -y install wget
rpm --import https://ca.mirror.babylon.network/epel/RPM-GPG-KEY-EPEL-7
wget https://ca.mirror.babylon.network/epel/epel-release-latest-7.noarch.rpm -O /tmp/epel.rpm
rpm -ivh /tmp/epel.rpm
wget https://dendory.net/scripts/nanorc -O /etc/nanorc
yum -y install nano scl-utils python34 python34-devel psmisc bind-utils python-pip python-devel libtool rpm-build
systemctl disable firewalld

#
# Install web server
#
yum -y install httpd php
systemctl enable httpd
systemctl start httpd
echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php

#
# Update the system
#
yum -y update
yum -y install yum-cron
reboot
