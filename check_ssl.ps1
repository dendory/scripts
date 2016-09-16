# This script checks a list of web sites and retrieves certificate information
#
# -Sites An array of web sites to check 
# -MinimumAge Warn if the certificate will expire in less than this amount of days (optional)
# -Timeout The timeout in seconds (optional)
#
# Example: .\check_ssl.ps1 -Sites @('https://google.com', 'https://yahoo.com') -MinimumAge 10
#
param([Parameter(Mandatory=$true)][string[]]$Sites, [Int32]$MinimumAge = 1, [Int32]$Timeout = 10)
$ErrorActionPreference = "Continue"
[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}

foreach ($site in $Sites)
{
	Write-Host "* Checking $site..."
	$req = [Net.HttpWebRequest]::Create($site)
	$req.Timeout = $Timeout * 1000
	try
	{
		$req.GetResponse() | Out-Null
		[datetime]$cert_exp = $req.ServicePoint.Certificate.GetExpirationDateString()
		$cert_thumb = $req.ServicePoint.Certificate.GetCertHashString()
		if($MinimumAge -gt ($cert_exp - $(get-date)).Days)
		{
			Write-Host "Error: Certificate expires on $cert_exp" -ForegroundColor red
		}
		else
		{
			Write-Host "Success: $cert_thumb" -ForegroundColor green
		}
	}
	catch
	{
		Write-Host "Error: $_" -ForegroundColor red
	}
}
