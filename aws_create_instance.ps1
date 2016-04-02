#
# This script will create an EC2 instance based on the configuration passed to it.
# Made by Patrick Lambert released under the MIT license.
#
# -AMI The Amazon image to use, for example CentOS for us-west-2 is available as ami-d2c924b2
# -Subnet The AWS subnet ID to use
# -Type The instance type, for example t2.nano
# -KeyName The connection key pair to use. The key must be saved in the current folder as $KeyName.pem if it exists, or will be created if not
# -Script File name for commands to run on startup
# -Hostname The hostname to add for this host
# -ZoneId The Route53 zone ID on which to add the hostname
# -SecurityGroup The security group ID to use for the new instance
#
param([Parameter(Mandatory=$true)][string]$AMI, [Parameter(Mandatory=$true)][string]$Subnet, [Parameter(Mandatory=$true)][string]$Type, [Parameter(Mandatory=$true)][string]$KeyName, [Parameter(Mandatory=$true)][string]$Script, [Parameter(Mandatory=$true)][string]$Hostname, [Parameter(Mandatory=$true)][string]$ZoneId, [Parameter(Mandatory=$true)][string]$SecurityGroup)
$ErrorActionPreference = "Stop"

# Make sure the key exists, otherwise create a new one
$keys = Get-EC2KeyPair
if($keys.KeyName -notcontains $KeyName)
{
  Write-Host "Creating key pair and saving to '$($KeyName).pem'..."
  $keypair1 = New-EC2KeyPair -KeyName $KeyName
  "$($keypair1.KeyMaterial)" | out-file -encoding ascii -filepath "$($KeyName).pem"
  "KeyName: $($keypair1.KeyName)" | out-file -encoding ascii -filepath "$($KeyName).pem" -Append
  "KeyFingerprint: $($keypair1.KeyFingerprint)" | out-file -encoding ascii -filepath "$($KeyName).pem" -Append
}

# Create the EC2 instance
Write-Host "Creating EC2 instance..."
$b = New-EC2Instance -ImageId $AMI -MinCount 1 -MaxCount 1 -KeyName $KeyName -SecurityGroupId $SecurityGroup -InstanceType $Type -SubnetId $Subnet -UserDataFile $Script -EncodeUserData
$new = $b.Instances[0].InstanceId

# Wait for it to run and get info
Write-Host "Instance $new created, waiting for running state..."
while($true)
{
  $a = Get-EC2Instance -Filter @{Name = "instance-id"; Value = $new} |select * -ExpandProperty Instances
  $state = $a.Instances[0].State.Name.Value
  if($state -eq "running")
  {
  break;
  }
  "Waiting..."
  Sleep -Seconds 5
}

$result = Get-EC2Instance -Filter @{Name = "instance-id"; Value = $new} |select * -ExpandProperty Instances
[string]$ip = $result.PublicIpAddress

# Add the A record to Route 53
Write-Host "Adding A record..."
$change = New-Object Amazon.Route53.Model.Change
$change.Action = "CREATE"
$change.ResourceRecordSet = New-Object Amazon.Route53.Model.ResourceRecordSet
$change.ResourceRecordSet.Name = $Hostname
$change.ResourceRecordSet.Type = "A"
$change.ResourceRecordSet.TTL = 600
$change.ResourceRecordSet.ResourceRecords.Add(@{Value=$ip})

Edit-R53ResourceRecordSet -HostedZoneId $ZoneId -ChangeBatch_Change $change

# Display result
Get-EC2Instance -Filter @{Name = "instance-id"; Value = $new} |select * -ExpandProperty Instances
Write-Host "Done."
