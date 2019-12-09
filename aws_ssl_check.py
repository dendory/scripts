#!/usr/bin/python3
# This script will enumerate all Route 53 hosts and EC2 instances, checking
# if any soon-to-expire SSL certificates can be found. Requires the pyopenssl
# library to be installed.

import os
import ssl
import json
import time
import boto3
import socket
from OpenSSL import crypto
from datetime import datetime


def get_expiry_days(hostname):
	""" Get the number of days before an ssl cert expires. """
	now = datetime.now()
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(3)
		if sock.connect_ex((hostname, 443)) != 0:
			return -1
		conn = ssl.create_connection((hostname, 443))
		context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
		sock = context.wrap_socket(conn, server_hostname=hostname)
		pem = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
		cert = crypto.load_certificate(crypto.FILETYPE_PEM, pem)
		expiry = datetime.strptime(cert.get_notAfter().decode('utf-8'), "%Y%m%d%H%M%SZ")
	except Exception:
		return -1
	return (expiry-now).days

def get_r53_hosts():
	""" Return a list of R53 hosts to check. """
	results = []
	client = boto3.client('route53', region_name='us-east-1')
	zones = client.list_hosted_zones()
	for zone in zones['HostedZones']:
		hosts = client.list_resource_record_sets(HostedZoneId=zone['Id'])
		for host in hosts['ResourceRecordSets']:
			if host['Type'] == "CNAME" and host['Name'][0] != '_':
				results.append(host['Name'])
	return results

def get_ec2_instances():
	""" Return a list of EC2 instances to check. """
	results = []
	client = boto3.client('ec2', region_name='us-east-1')
	regions = client.describe_regions()['Regions']
	for region in regions:
		ec2 = boto3.resource("ec2", region_name=region['RegionName'])
		for i in ec2.instances.filter():
			results.append(i.network_interfaces_attribute[0]['PrivateIpAddress'])
	return results


for host in get_ec2_instances():
	expiry = get_expiry_days(host)
	if expiry < 1:
		print("The SSL certificate of {} is expired or cannot be checked!".format(host))
	else:
		print("The SSL certificate of {} expires in {} days.".format(host, expiry))

for host in get_r53_hosts():
	expiry = get_expiry_days(host)
	if expiry < 1:
		print("The SSL certificate of {} is expired or cannot be checked!".format(host))
	else:
		print("The SSL certificate of {} expires in {} days.".format(host, expiry))
