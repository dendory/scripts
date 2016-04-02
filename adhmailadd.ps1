Import-Module ActiveDirectory
# This script creates an Active Directory user and an hMailServer user
# (C) 2015 Patrick Lambert provided under MIT license - http://dendory.net
#
# The Active Directory domain to use:
#
$domain = Get-ADDomain
#
# The base DN for accounts (DC=example,DC=com):
#
$dn = $domain.DistinguishedName
#
# The domain used for emails (example.com):
#
$dnsroot = $domain.DNSRoot;
#
# Enter your hMailServer password here:
#
$hmail_password = "xxxxxxxxxxxxxxx"
#
# Max size of account mailbox (in megs):
#
$hmail_maxsize = 100
#
# End of configuration
#
$letters = 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
$symbols = '!','?','*','&','%','$','#'
do 
{
	Write-Host "AD HMAIL ADD - (C) 2015 Patrick Lambert - http://dendory.net"
	Write-Host
	do { $cn = Read-Host "User ID" } while($cn -eq "")
	do { $fn = Read-Host "First name" } while($fn -eq "")
	do { $ln = Read-Host "Last name" } while($ln -eq "")
	$ou = Read-Host "Organizational unit [default: List available OUs]"
	if($ou -eq "")
	{
		Get-ADOrganizationalUnit -Filter * | Select Name | Format-Table
		do { $ou = Read-Host "Organizational unit" } while($ou -eq "")
		if($ou -eq "") { $ou = "Users" }
	}
	$defemail = "$fn.$ln@$dnsroot"
	$defemail = $defemail -replace '\s',''
	$email = Read-Host "Email address [default: $defemail]"
	if($email -eq "") { $email = $defemail }
	$upn = "$cn@$dnsroot"
	# Doing ran this way to ensure we have letters, symbols and numbers. Should find a way to mix them more securely
	$ran = $letters | Get-Random
	$ran += $letters | Get-Random
	$ran += $letters | Get-Random
	$ran += $symbols | Get-Random
	$ran += $letters | Get-Random
	$ran += $letters | Get-Random
	$ran += $letters | Get-Random
	$ran += $symbols | Get-Random
	$ran += Get-Random -minimum 1000 -maximum 9999
	$pwd = Read-Host "Initial password [default: $ran]"
	if($pwd -eq "") { $pwd = $ran }
	Write-Host
	Write-Host "* Adding AD account..."
	# Any specific additional attribute for dsadd can be added here
	dsadd user "CN=$cn,OU=$ou,$dn" -upn "$upn" -email "$email" -fn "$fn" -ln "$ln" -pwd $pwd -display "$fn $ln" -disabled no
	Write-Host "* Adding hMailServer account..."
	# This creates a COM object against the hMailServer API
	$hm = New-Object -ComObject hMailServer.Application
	$hm.Authenticate("Administrator", $hmail_password) | Out-Null
	$hmdom = $hm.Domains.ItemByName($dnsroot)
	$hmact = $hmdom.Accounts.Add()
	# Filling attributes for the email account based on current information, including AD integration for the password
	$hmact.Address = $email
	$hmact.Active = $true
	$hmact.IsAD = $true
	$hmact.MaxSize = $hmail_maxsize
	$hmact.ADDomain = $dn
	$hmact.ADUsername = $cn
	$hmact.PersonFirstName = $fn
	$hmact.PersonLastName = $ln
	$hmact.save()
	Write-Host "Done."
	Read-Host "Press ENTER to add another user, CTRL-C to quit"
	cls
}
while($true)
