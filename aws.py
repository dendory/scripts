#!/usr/bin/python3
#
# Simple AWS automation script - Patrick Lambert - http://dendory.net
# Prerequisites: `pip3 install boto3` and `aws configure`
#
import os
import sys
import json
import time
cfgfile = os.path.join(os.path.expanduser("~"), ".aws.templates")

#
# Internal functions
#
def fail(msg):
	if os.name != "nt":
		print("\033[91m* " + msg + "\033[0m")
	else:
		print("[ERROR] " + msg)

def success(msg):
	if os.name != "nt":
		print("\033[92m* " + msg + "\033[0m")
	else:
		print("[SUCCESS] " + msg)

def info(msg):
	if os.name != "nt":
		print("\033[94m* " + msg + "\033[0m")
	else:
		print("[INFO] " + msg)

def ask(msg, default):
	tmp = input(msg + " [" + str(default) + "]: ")
	if tmp == "":
		return default
	if type(True) == type(default) and str(tmp).lower() == "true":
		return True
	elif type(False) == type(default) and str(tmp).lower() == "false":
		return False
	elif type(int(2)) == type(default):
		return int(tmp)
	else:
		return tmp

def load_templates():
	templates = []
	try:
		f = open(cfgfile, 'r')
		rows = json.loads(f.read())
		f.close()
		for row in rows:
			if "name" in row.keys():
				templates.append(row)
	except:
		pass
	return templates

def save_templates(templates):
	try:
		f = open(cfgfile, 'w')
		f.write(json.dumps(templates))
		f.close()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not save templates file: " + str(b))
		return False

def usage():
	info("Usage: aws.py <command> [options]")
	print()
	info("Available commands:")
	print("list-vms [-v|instance id|name]                        : List all VMs, or details on one VM")
	print("start-vm <instance id|name>                           : Start a VM")
	print("stop-vm <instance id|name>                            : Stop a VM")
	print("restart-vm <instance id|name>                         : Reboot a VM")
	print("delete-vm <instance id>                               : Terminate a VM")
	print("set-tag <instance id|name> <tag> <value>              : Change the tag of a VM")
	print("list-templates [-v]                                   : List existing templates")
	print("create-template                                       : Create a new VM template")
	print("create-vm <vm name|%> <template to use> [-w]          : Create a new VM based on a template")
	print("dump-inventory <file> [filter]                        : Put all internal IPs in a text file")
	print("get-password <instance id|name> [key file]            : Retrieve the password of a Windows VM")
	print("create-volume <instance id> <device name> <size in GB>: Create a new volume and attach to a VM")
	print("attach-volume <instance id> <device name> <volume id> : Attach an existing volume to a VM")
	print("detach-volume <volume id>                             : Detach a volume from a VM")
	print("delete-volume <volume id>                             : Delete a detached volume")
	print("create-snapshot <instance id> <description>           : Create a snapshot of all attached volumes")
	print("delete-snapshot <snapshot id>                         : Delete an existing snapshot")
	print("list-dns-zones [-v]                                   : List hosted zones in Route53")
	print("list-dns-records <zone id>                            : List record sets in a zone")
	print("create-dns-record <zone id> <name> <type> <value>     : Create a record set")
	print("delete-dns-record <zone id> <name> <type> <value>     : Delete a record set")
	print("list-public-ips                                       : List current elastic IPs")
	print("create-public-ip                                      : Allocate a new elastic IP")
	print("delete-public-ip <address id>                         : Revoke an elastic IP")
	print("attach-public-ip <address id> <instance id|name>      : Attach an IP to a VM")
	print("detach-public-ip <address id>                         : Detach an IP from a VM")
	print("list-load-balancers                                   : List all load balancers")
	print("attach-balanced-vm <balancer id> <instance id|name>   : Attach a VM to a load balancer")
	print("detach-balanced-vm <balancer id> <instance id|name>   : Detach a VM from a load balancer")

#
# AWS operations
#
def create_snapshot(volid, desc):
	try:
		ec2 = boto3.resource("ec2")
		snapshot = ec2.create_snapshot(VolumeId=volid, Description=desc)
		return snapshot.id
	except:
		a, b, c = sys.exc_info()
		fail("Could not create snapshot: " + str(b))
		return None

def delete_snapshot(snapid):
	try:
		ec2 = boto3.resource("ec2")
		snapshot = ec2.Snapshot(snapid)
		snapshot.delete()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not delete snapshot: " + str(b))
		return False

def start_vm(instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.resource("ec2")
		instance = ec2.Instance(instid)
		instance.start()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not start VM: " + str(b))
		return False

def list_hosted_zones():
	try:
		r53 = boto3.client("route53")
		zones = r53.list_hosted_zones()
		return zones['HostedZones']
	except:
		a, b, c = sys.exc_info()
		fail("Could not list hosted zone: " + str(b))
		return []

def list_record_sets(zoneid):
	try:
		r53 = boto3.client("route53")
		sets = r53.list_resource_record_sets(HostedZoneId=zoneid)
		return sets['ResourceRecordSets']
	except:
		a, b, c = sys.exc_info()
		fail("Could not list record sets: " + str(b))
		return []

def stop_vm(instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.resource("ec2")
		instance = ec2.Instance(instid)
		instance.stop()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not stop VM: " + str(b))
		return False

def attach_ip(ipid, instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.client("ec2")
		resp = ec2.associate_address(InstanceId=instid, AllocationId=ipid)
		return resp['AssociationId']
	except:
		a, b, c = sys.exc_info()
		fail("Could not associate IP: " + str(b))
		return None

def detach_ip(ipid):
	try:
		ec2 = boto3.client("ec2")
		ips = list_ips()
		for ip in ips:
			if ip['AllocationId'] == ipid and "AssociationId" in ip:
				resp = ec2.disassociate_address(AssociationId=ip['AssociationId'])
				return True
		print("No association found.")
		return False
	except:
		a, b, c = sys.exc_info()
		fail("Could not detach IP: " + str(b))
		return False

def restart_vm(instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.resource("ec2")
		instance = ec2.Instance(instid)
		instance.reboot()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not restart VM: " + str(b))
		return False

def get_password(instid, keyfile):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.client("ec2")
		data = ec2.get_password_data(InstanceId=instid)
		if data['PasswordData'] == "":
			return ""
		if keyfile:
			cmd = "echo \"" + "".join(data['PasswordData'].split()) + "\" |base64 -d |openssl rsautl -decrypt -inkey \"" + keyfile + "\""
			return os.popen(cmd).read()
		else:
			return data['PasswordData']
	except:
		a, b, c = sys.exc_info()
		fail("Could not fetch password: " + str(b))
		return None

def delete_vm(instid):
	try:
		ec2 = boto3.resource("ec2")
		instance = ec2.Instance(instid)
		instance.terminate()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not terminate VM: " + str(b))
		return False

def create_vm(name, template, dowait):
	try:
		ec2 = boto3.resource("ec2")
		info("Creating instance...")
		devmap = [{"DeviceName": template['volume name'], "Ebs": {"VolumeSize": int(template['volume size']), "VolumeType": "gp2"}}]
		content = ""
		if template['script'] != "":
			f = open(template['script'], 'r')
			content = f.read()
			f.close()
		instance = ec2.create_instances(ImageId = template['ami'], MinCount = 1, MaxCount = 1, KeyName = template['key'], SecurityGroupIds = [template['security group']], InstanceType = template['type'], BlockDeviceMappings = devmap, SubnetId = template['subnet'], UserData = content)
		instance = instance[0]
		print("Instance ID: " + instance.id)
		print("Private IP: " + instance.private_ip_address)
		ec2.create_tags(Resources = [instance.id], Tags = [{'Key': 'Name', 'Value': name.replace('%',instance.private_ip_address.split('.')[3])}])
		if dowait:
			info("Waiting for running state...")
			instance.wait_until_running()
		return instance.id
	except:
		a, b, c = sys.exc_info()
		fail("Could not create VM: " + str(b))
		return None

def set_tag(instid, key, value):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.resource("ec2")
		ec2.create_tags(Resources = [instid], Tags = [{'Key': key, 'Value': value}])
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not set tag: " + str(b))
		return False

def new_ip():
	try:
		ec2 = boto3.client("ec2")
		return ec2.allocate_address(DryRun=False, Domain='vpc')
	except:
		a, b, c = sys.exc_info()
		fail("Could not allocate IP: " + str(b))
		return None

def revoke_ip(addrid):
	try:
		ec2 = boto3.client("ec2")
		ec2.release_address(DryRun=False, AllocationId=addrid)
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not revoke IP: " + str(b))
		return False

def list_ips():
	try:
		ec2 = boto3.client("ec2")
		ips = ec2.describe_addresses()
		return ips['Addresses']
	except:
		a, b, c = sys.exc_info()
		fail("Could not list IPs: " + str(b))
		return []

def list_elb():
	try:
		ec2 = boto3.client("elb")
		lbs = ec2.describe_load_balancers()
		return lbs['LoadBalancerDescriptions']
	except:
		a, b, c = sys.exc_info()
		fail("Could not list load balancers: " + str(b))
		return []

def attach_elb(elbid, instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.client("elb")
		ec2.register_instances_with_load_balancer(LoadBalancerName=elbid, Instances=[{'InstanceId': instid}])
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not attach instance to load balancer: " + str(b))
		return False

def detach_elb(elbid, instid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.client("elb")
		ec2.deregister_instances_from_load_balancer(LoadBalancerName=elbid, Instances=[{'InstanceId': instid}])
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not detach instance from load balancer: " + str(b))
		return False

def create_volume(zone, size):
	try:
		ec2 = boto3.resource("ec2")
		volume = ec2.create_volume(Size=size, VolumeType='gp2', AvailabilityZone=zone)
		return volume.id
	except:
		a, b, c = sys.exc_info()
		fail("Could not create volume: " + str(b))
		return None

def detach_volume(volid):
	try:
		ec2 = boto3.resource("ec2")
		volume = ec2.Volume(volid)
		volume.detach_from_instance()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not detach volume: " + str(b))
		return False

def change_record_set(zoneid, oper, rrn, rrt, rrv):
	try:
		r53 = boto3.client("route53")
		response = r53.change_resource_record_sets(HostedZoneId = zoneid, ChangeBatch={'Comment': 'aws.py scripted change', 'Changes': [{'Action': oper, 'ResourceRecordSet': {'Name': rrn, 'Type': rrt, 'GeoLocation': {}, 'SetIdentifier': 'aws.py updated record', 'TTL': 60, 'ResourceRecords': [{'Value': rrv}]}}]})
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not set record: " + str(b))
		return False

def delete_volume(volid):
	try:
		ec2 = boto3.resource("ec2")
		volume = ec2.Volume(volid)
		volume.delete()
		return True
	except:
		a, b, c = sys.exc_info()
		fail("Could not delete volume: " + str(b))
		return False

def attach_volume(instid, devicename, volid):
	try:
		if instid[0:1] != "i-":
			for ins in list_vms():
				if ins['name'] == instid:
					instid = ins['id']
		ec2 = boto3.resource("ec2")
		instance = ec2.Instance(instid)
		x = 0
		while True:
			volume = ec2.Volume(volid)
			if volume.state == 'available':
				break
			time.sleep(1)
			x += 1
			if x > 5:
				fail("Volume state: " + volume.state)
				return None
		instance.attach_volume(VolumeId=volid, Device=devicename)
		return volume.id
	except:
		a, b, c = sys.exc_info()
		fail("Could not attach volume: " + str(b))
		return None

def list_vms():
	try:
		vms = []
		ec2 = boto3.resource("ec2")
		for i in ec2.instances.filter():
			name = ""
			if i.tags:
				for tag in i.tags:
					if tag['Key'] == "Name":
						name = tag['Value']
			vols = []
			snaps = []
			for vol in i.volumes.all():
				for attach in vol.attachments:
					vols.append({'id': vol.id, 'size': vol.size, 'device': attach['Device']})
				for snap in vol.snapshots.all():
					snaps.append({'id': snap.id, 'volume': snap.volume_id})
			sgs = []
			for sg in i.security_groups:
				sgs.append(sg['GroupId'])
			vms.append({'id': i.instance_id, 'type': i.instance_type, 'arch': i.architecture, 'ami': i.image_id, 'created': str(i.launch_time), 'public ip': i.public_ip_address, 'private ip': i.private_ip_address, 'key': i.key_name, 'subnet': i.subnet_id, 'state': i.state['Name'], 'vpc': i.vpc_id, 'name': name, 'volumes': vols, 'security groups': sgs, 'snapshots': snaps, 'zone': i.placement['AvailabilityZone']})
		return vms
	except:
		a, b, c = sys.exc_info()
		fail("Could not list VMs: " + str(b))
		return []

#
# Main
#
try:
	import boto3
except:
	fail("Please install the AWS API and configure your API credentials first:")
	print("pip3 install boto3")
	print("aws configure")
	quit(1)

if len(sys.argv) < 2:
	usage()
	quit(1)

if sys.argv[1].lower() == 'list-vms':
	for i in list_vms():
		if len(sys.argv) > 2 and sys.argv[2].lower() == "-v":
			info(i['name'] + " (" + i['id'] + "): " + i['state'])
			for key in i.keys():
				print(key + ": " + str(i[key]))
		elif len(sys.argv) > 2:
			if i['id'].lower() == sys.argv[2].lower():
				info(i['name'] + " (" + i['id'] + "): " + i['state'])
				for key in i.keys():
					print(key + ": " + str(i[key]))
		else:
			print(i['name'] + " (" + i['id'] + "): " + i['state'])
elif sys.argv[1].lower() == 'dump-inventory':
	if len(sys.argv) < 3:
		fail("Invalid number of arguments")
	else:
		f = open(sys.argv[2], 'a')
		for i in list_vms():
			if len(sys.argv) > 3:
				if sys.argv[3].lower() in i['name'].lower():
					f.write(i['private ip'] + "\n")
			else:
				f.write(i['private ip'] + "\n")
		f.close()
		success("Done.")
elif sys.argv[1].lower() == 'create-snapshot':
	if len(sys.argv) != 4:
		fail("Invalid number of arguments")
	else:
		for i in list_vms():
			if i['id'] == sys.argv[2].lower():
				for v in i['volumes']:
					print(v['id'] + ": " + create_snapshot(v['id'], sys.argv[3]))
		success("Done.")
elif sys.argv[1].lower() == 'delete-snapshot':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if delete_snapshot(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'start-vm':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if start_vm(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'stop-vm':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if stop_vm(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'restart-vm':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if restart_vm(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'get-password':
	if len(sys.argv) == 3:
		print(get_password(sys.argv[2], None))
	elif len(sys.argv) == 4:
		print(get_password(sys.argv[2], sys.argv[3]))
	else:
		fail("Invalid number of arguments")
elif sys.argv[1].lower() == 'set-tag':
	if len(sys.argv) != 5:
		fail("Invalid number of arguments")
	else:
		if set_tag(sys.argv[2], sys.argv[3], sys.argv[4]):
			success("Done.")
elif sys.argv[1].lower() == 'delete-vm':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if delete_vm(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'list-templates':
	for i in load_templates():
		if len(sys.argv) > 2 and sys.argv[2].lower() == "-v":
			info(i['name'] + " (" + i['ami'] + "): " + i['description'])
			for key in i.keys():
				print(key + ": " + str(i[key]))
		else:
			print(i['name'] + " (" + i['ami'] + "): " + i['description'])
elif sys.argv[1].lower() == 'create-template':
	tmpl = {}
	templates = load_templates()
	tmpl['name'] = ask("Unique template name", "default")
	for t in templates:
		if t['name'] == tmpl['name']:
			fail("Name already exists.")
			quit(1)
	tmpl['description'] = ask("Description", "Very small CentOS instance")
	tmpl['ami'] = ask("AMI image", "ami-d440a6e7")
	tmpl['type'] = ask("Instance type", "t2.nano")
	tmpl['security group'] = ask("Security group", "sg-1234567")
	tmpl['volume name'] = ask("Volume device to attach", "/dev/xvda")
	tmpl['volume size'] = ask("Volume size in gigabytes", 30)
	tmpl['subnet'] = ask("Subnet id", "subnet-a1b2c3")
	tmpl['script'] = ask("Script file to run on creation", "")
	tmpl['key'] = ask("Connection key name", "my-key")
	templates.append(tmpl)
	if save_templates(templates):
		success("Done.")
elif sys.argv[1].lower() == 'create-vm':
	if len(sys.argv) < 4:
		fail("Invalid number of arguments")
	else:
		tmpls = load_templates()
		for tmpl in tmpls:
			if tmpl['name'].lower() == sys.argv[3].lower():
				if len(sys.argv) == 4:
					if create_vm(sys.argv[2], tmpl, False):
						success("Done.")
				else:
					if create_vm(sys.argv[2], tmpl, True):
						success("Done.")
elif sys.argv[1].lower() == 'create-volume':
	if len(sys.argv) != 5:
		fail("Invalid number of arguments")
	else:
		info("Creating volume...")
		for i in list_vms():
			if i['id'].lower() == sys.argv[2].lower():
				volume = create_volume(i['zone'], int(sys.argv[4]))
				if volume:
					print("Volume ID: " + volume)
					info("Attaching volume...")
					if attach_volume(i['id'], sys.argv[3], volume):
						success("Done.")
elif sys.argv[1].lower() == 'detach-volume':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if detach_volume(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'delete-volume':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if delete_volume(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'attach-volume':
	if len(sys.argv) != 5:
		fail("Invalid number of arguments")
	else:
		if attach_volume(sys.argv[2], sys.argv[3], sys.argv[4]):
			success("Done.")
elif sys.argv[1].lower() == 'list-dns-zones':
	zones = list_hosted_zones()
	if len(sys.argv) == 2:
		for zone in zones:
			print(zone['Id'].replace('/hostedzone/','') + ": " + zone['Name'])
	else:
		for zone in zones:
			info(zone['Id'].replace('/hostedzone/','') + ": " + zone['Name'])
			sets = list_record_sets(zone['Id'])
			for set in sets:
				if "ResourceRecords" in set:
					for rr in set['ResourceRecords']:
						print(set['Name'] + " " + set['Type'] + " : " + rr['Value'])
				elif "AliasTarget" in set:
					print(set['Name'] + " " + set['Type'] + " : ALIAS " + set['AliasTarget']['DNSName'])
elif sys.argv[1].lower() == 'list-dns-records':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		sets = list_record_sets(sys.argv[2])
		for set in sets:
			if "ResourceRecords" in set:
				for rr in set['ResourceRecords']:
					print(set['Name'] + " " + set['Type'] + " : " + rr['Value'])
			elif "AliasTarget" in set:
				print(set['Name'] + " " + set['Type'] + " : ALIAS " + set['AliasTarget']['DNSName'])
elif sys.argv[1].lower() == 'create-dns-record':
	if len(sys.argv) != 6:
		fail("Invalid number of arguments")
	else:
		if change_record_set(sys.argv[2], "CREATE", sys.argv[3], sys.argv[4], sys.argv[5]):
			success("Done.")
elif sys.argv[1].lower() == 'delete-dns-record':
	if len(sys.argv) != 6:
		fail("Invalid number of arguments")
	else:
		if change_record_set(sys.argv[2], "DELETE", sys.argv[3], sys.argv[4], sys.argv[5]):
			success("Done.")
elif sys.argv[1].lower() == 'create-public-ip':
	ip = new_ip()
	if ip:
		success(ip['AllocationId'] + ": " + ip['PublicIp'])
elif sys.argv[1].lower() == 'delete-public-ip':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if revoke_ip(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'attach-public-ip':
	if len(sys.argv) != 4:
		fail("Invalid number of arguments")
	else:
		print(attach_ip(sys.argv[2], sys.argv[3]))
elif sys.argv[1].lower() == 'detach-public-ip':
	if len(sys.argv) != 3:
		fail("Invalid number of arguments")
	else:
		if detach_ip(sys.argv[2]):
			success("Done.")
elif sys.argv[1].lower() == 'list-public-ips':
	ips = list_ips()
	for ip in ips:
		if "InstanceId" in ip:
			print(ip['AllocationId'] + " (" + ip['PublicIp'] + "): " + ip['InstanceId'])
		elif "NetworkInterfaceId" in ip:
			print(ip['AllocationId'] + " (" + ip['PublicIp'] + "): " + ip['NetworkInterfaceId'])
		else:
			print(ip['AllocationId'] + " (" + ip['PublicIp'] + "): Not associated.")
elif sys.argv[1].lower() == 'list-load-balancers':
	lbs = list_elb()
	for lb in lbs:
		if "Instances" in lb:
			print(lb['LoadBalancerName'] + " (" + lb['CanonicalHostedZoneName'] + "): ", end="")
			for i in lb['Instances']:
				print(i['InstanceId'] + " ", end="")
			print()
		else:
			print(lb['LoadBalancerName'] + " (" + lb['CanonicalHostedZoneName'] + "): No instance attached.")
elif sys.argv[1].lower() == 'attach-balanced-vm':
	if len(sys.argv) != 4:
		fail("Invalid number of arguments")
	else:
		if attach_elb(sys.argv[2], sys.argv[3]):
			success("Done.")
elif sys.argv[1].lower() == 'detach-balanced-vm':
	if len(sys.argv) != 4:
		fail("Invalid number of arguments")
	else:
		if detach_elb(sys.argv[2], sys.argv[3]):
			success("Done.")
else:
	fail("Unknown command: " + sys.argv[1])
	usage()
	quit(1)

