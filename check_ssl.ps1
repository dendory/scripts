# This script returns information about a site's SSL certificate
#
# -URL The URL to check
# -Timeout The timeout in seconds (optional)
#
param([Parameter(Mandatory=$true)][string]$URL, [Int32]$Timeout = 10)
$ErrorActionPreference = "Continue"
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}

$req = [System.Net.HttpWebRequest]::Create($URL)
$req.Timeout = $Timeout * 1000
$req.GetResponse() | Out-Null
$Certificate = New-Object PSObject
$Certificate | Add-Member -NotePropertyName "Name" -NotePropertyValue $req.ServicePoint.Certificate.GetName()
$Certificate | Add-Member -NotePropertyName "Issuer" -NotePropertyValue $req.ServicePoint.Certificate.GetIssuerName()
$Certificate | Add-Member -NotePropertyName "Expiration" -NotePropertyValue $req.ServicePoint.Certificate.GetExpirationDateString()
$Certificate | Add-Member -NotePropertyName "Thumbnail" -NotePropertyValue $req.ServicePoint.Certificate.GetCertHashString()
$Certificate | Add-Member -NotePropertyName "Serial Number" -NotePropertyValue $req.ServicePoint.Certificate.GetSerialNumberString()
$Certificate | Add-Member -NotePropertyName "Public Key" -NotePropertyValue $req.ServicePoint.Certificate.GetPublicKeyString()
$Certificate
