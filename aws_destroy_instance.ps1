#
# This script will terminate an EC2 instance based on the configuration passed to it.
# Made by Patrick Lambert released under the MIT license.
#
# Prerequisites:
# 1- Download the AWS PowerShell tools from: http://aws.amazon.com/powershell
# 2- Create an IAM user with the Route 53 all api access policy enabled
# 3- Store your IAM user credentials locally: Set-AWSCredentials -AccessKey XXXXX -SecretKey ZZZZZ -StoreAs default
#
# -InstanceId The EC2 instance id to terminate
# -Hostname The hostname to remove for this host
# -ZoneId The Route53 zone ID on which to remove the hostname
#
param([Parameter(Mandatory=$true)][string]$InstanceId, [Parameter(Mandatory=$true)][string]$Hostname, [Parameter(Mandatory=$true)][string]$ZoneId)
$ErrorActionPreference = "Stop"

# Fetch the EBS drive id and IP address
$result = Get-EC2Instance -Filter @{Name = "instance-id"; Value = $InstanceId} |select * -ExpandProperty Instances
[string]$ip = $result.PublicIpAddress
$volumes = Get-EC2Volume -Filter @{ Name = "attachment.instance-id"; Value = $InstanceId }

# Terminate the instance
Write-Host "Terminating instance $Instance..."
Stop-EC2Instance $InstanceId -Force -Terminate

# Remove the EBS
foreach($volume in $volumes)
{
	[string]$volid = $volume.VolumeId
	Write-Host "Removing EBS volume $volid..."
	Remove-EC2Volume -VolumeId $volid -Force
}

# Remove A record
Write-Host "Removing A record..."
$change = New-Object Amazon.Route53.Model.Change
$change.Action = "DELETE"
$change.ResourceRecordSet = New-Object Amazon.Route53.Model.ResourceRecordSet
$change.ResourceRecordSet.Name = $Hostname
$change.ResourceRecordSet.Type = "A"
$change.ResourceRecordSet.TTL = 600
$change.ResourceRecordSet.ResourceRecords.Add(@{Value=$ip})

Edit-R53ResourceRecordSet -HostedZoneId $ZoneId -ChangeBatch_Change $change

# Done
Write-Host "Done."
