#!/bin/bash

#
# Remove SSL support and LetsEncrypt
#

yum -y remove python-certbot-apache certbot mod_ssl
mv /etc/httpd/conf/httpd.default /etc/httpd/conf/httpd.conf
systemctl restart httpd
