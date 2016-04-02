# This script lists records for all AWS Route53 hosted zones
#
# Prerequisites:
# 1- Download the AWS PowerShell tools from: http://aws.amazon.com/powershell
# 2- Create an IAM user with the Route 53 all api access policy enabled
# 3- Store your IAM user credentials locally: Set-AWSCredentials -AccessKey XXXXX -SecretKey ZZZZZ -StoreAs default
#
Param([string]$Domain = "", [string]$Type = "*")

Import-Module AWSPowerShell

$zones = Get-R53HostedZones

foreach($zone in $zones)
{
    if($Domain -eq "" -or $zone.Name -eq "$Domain.")
    {
        $(Get-R53ResourceRecordSet -HostedZoneId $($zone.Id)).ResourceRecordSets | Where {$_.Type -like $Type} | Select Name,Type,@{Name='Value';Expression={$_.ResourceRecords | Select -ExpandProperty Value}}
    }
}
