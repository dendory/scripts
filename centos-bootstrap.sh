#!/bin/bash
# CentOS 7 bootstrapping script - Configuration:

export NAME=%NAME%
export DOMAIN=dendory.net
export EMAIL=dendory@live.ca

#
# Set hostname and networking
#
echo "$NAME.$DOMAIN" > /etc/hostname
chattr +i /etc/hostname
echo "search $DOMAIN" > /etc/resolv.conf
echo "domain $DOMAIN" >> /etc/resolv.conf
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
# Install EPEL, Nux and missing packages
#
yum -y install wget
rpm --import https://ca.mirror.babylon.network/epel/RPM-GPG-KEY-EPEL-7
wget https://ca.mirror.babylon.network/epel/epel-release-latest-7.noarch.rpm -O /tmp/epel.rpm
rpm -ivh /tmp/epel.rpm
rm -f /tmp/epel.rpm
rpm --import http://li.nux.ro/download/nux/RPM-GPG-KEY-nux.ro
rpm -Uvh http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-1.el7.nux.noarch.rpm
wget https://dendory.net/scripts/nanorc -O /etc/nanorc
yum -y install nano scl-utils python34 python34-devel psmisc bind-utils python-pip python-devel libtool rpm-build ffmpeg ImageMagick ImageMagick-devel ntp
curl https://bootstrap.pypa.io/get-pip.py | python3
rm -f /usr/bin/pip
ln -s /usr/bin/pip2.7 /usr/bin/pip
pip install mutagen ansible awscli certbot evernote Markdown MySQL-python
pip3 install pycrypto boto3 connix
python3 -m pip install -U discord.py
systemctl disable firewalld
systemctl start ntpd

#
# Install web server
#
yum -y install httpd php
systemctl enable httpd
systemctl start httpd
echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php

#
# Install SSL support and LetsEncrypt
#
RESOLVED=`getent hosts $NAME.$DOMAIN`
if [ ! -z "$RESOLVED" ]; then
	yum -y install python-certbot-apache certbot mod_ssl
	letsencrypt certonly --standalone --email $EMAIL -d $NAME.$DOMAIN -w /var/www/html --agree-tos --renew-by-default -n
	mv /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.default
	wget https://dendory.net/scripts/centos-httpd-ssl.conf -O /etc/httpd/conf/httpd.conf
	sed -i "s/%HOSTNAME%/$NAME.$DOMAIN/g" /etc/httpd/conf/httpd.conf
	systemctl restart httpd
	crontab -l > /tmp/mycron
	echo "0 0 1 * * /usr/sbin/certbot renew" >> /tmp/mycron
	crontab /tmp/mycron
	rm -f /tmp/mycron
fi

#
# Update the system
#
yum -y update
yum -y install yum-cron
reboot

