# This script will check a web site every 10 secs for availability, and alert you if it becomes unavailable or returns an error code

param([Parameter(Mandatory=$true)][string]$URL, [Int32]$Timeout = 10)
$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Windows.Forms
while($true)
{
	try 
	{
		$code = (Invoke-WebRequest -Uri $URL).StatusCode
		if ($code -ne 200)
		{
			[System.Windows.Forms.MessageBox]::Show("Alert: Website returned an error code! [" + $code + "]")
			exit
		}
	}
	catch
	{
		[System.Windows.Forms.MessageBox]::Show("Alert: Could not connect to website! [" + $_ + "]")
		exit
	}
	Start-Sleep -s $Timeout
}
