# Shows a graphical list of user logins.
param([int] $MaxEvents = 100, [string]$ComputerName = "" , [string]$Credential = "", [string] $Filter = "")

Write-Host "logins.ps1 - (C) 2015 Patrick Lambert - http://dendory.net"
Write-Host "This script must be run from an administrative PowerShell prompt and requires PowerShell-ISE to be installed."
Write-Host "Usage: logins.ps1 [-MaxEvents <number>] [-ComputerName <hostname>] [-Filter <word>]"
Write-Host "Fetching data..."

if($ComputerName )
{
	$Events = Get-WinEvent -ComputerName $ComputerName -Credential $Credential -FilterHashtable @{Logname= 'Security';Id= 4624,4625 ;Data=$Filter } -MaxEvents $MaxEvents
}
else
{
	$Events = Get-WinEvent -FilterHashtable @{Logname='Security';Id =4624, 4625;Data= $Filter} -MaxEvents $MaxEvents
}

ForEach ($Event in $Events)
{
	$eventXML = [xml]$Event.ToXml()
	For ($i =0; $i -lt $eventXML.Event.EventData.Data.Count; $i++)
	{
		Add-Member -InputObject $Event -MemberType NoteProperty -Force -Name $eventXML.Event.EventData.Data[$i].name -Value $eventXML.Event.EventData.Data[$i].'#text'
	}
}

$Events | Select-Object @{Name ="ID";Expression ={$_.RecordId}}, @{Name="Login time";Expression ={$_.TimeCreated}}, @{Name="Event" ;Expression={ $_.Id -Replace "4625","Failure" -Replace "4624","Success" }},@{Name ="Reason";Expression ={$_.Status -Replace "0xc0000064","User does not exist" -Replace "0xc000006a","Invalid password" -Replace "0xc000006d","Bad user name or password" -Replace "0xc0000234","Account is locked out" -Replace "0xc0000072","Account is disabled" -Replace "0xc000006f","Time or date restrictions" -Replace "0xc0000070","Workstation restrictions" -Replace "0xc0000193","Account expired" -Replace "0xc0000071","Password expired" -Replace "0xc0000133","Clock is out of sync" -Replace "0xc0000224","User must change password" -Replace "0xc0000225","Windows bug" -Replace "0xc000015b","No login rights" -Replace "0xc000018c","Domain trust relationship failed" -Replace "0xc000005e","Domain controller unavailable" -Replace "0xc00000dc","Bad state" -Replace "0xc0000192","Netlogon service missing" -Replace "0xc0000413","Account login unauthorized" -Replace "0x8009030e","Cannot reach IP-HTTPS server"}},@{Name ="Process Name";Expression ={$_.LogonProcessName}}, @{Name="Login Type";Expression ={$_.LogonType -Replace "11","Cached credentials" -Replace "10","Remote access" -Replace "9","Run as" -Replace "8","Network access (clear text)" -Replace "7","Unlocked workstation" -Replace "5","Service access" -Replace "4","Batch script" -Replace "3","Network access" -Replace "2","Interactive" }},@{Name ="Workstation";Expression ={$_.WorkstationName}}, @{Name="IP Address" ;Expression={ $_.IpAddress}} ,@{Name="Subject Domain";Expression ={$_.SubjectDomainName}}, @{Name="Subject User";Expression ={$_.SubjectUserName}}, @{Name="Target Domain";Expression ={$_.TargetDomainName}}, @{Name="Target User";Expression ={$_.TargetUserName}} | Out-GridView -Title "Last $MaxEvents logins"
 
