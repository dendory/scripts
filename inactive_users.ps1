# Lists all AD users who haven't logged in 90 days

$time = (Get-Date).Adddays(-90); Get-ADUser -Filter {LastLogonTimeStamp -lt $time -and enabled -eq $true} -Properties LastLogonTimestamp | Select Name,@{Name="Last Logon";Expression={[DateTime]::FromFileTime($_.LastLogonTimestamp).ToString('yyyy-MM-dd hh:mm:ss')}}
$time
