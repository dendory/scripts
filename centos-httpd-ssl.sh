#!/bin/bash

#
# Install SSL support and LetsEncrypt
#

yum -y install python-certbot-apache certbot mod_ssl
letsencrypt certonly --standalone --email dendory@live.ca -d $HOSTNAME -w /var/www/html
mv /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.default
wget https://dendory.net/scripts/centos-httpd-ssl.conf -O /etc/httpd/conf/httpd.conf
sed -i "s/%HOSTNAME%/$HOSTNAME/g" /etc/httpd/conf/httpd.conf
systemctl restart httpd
