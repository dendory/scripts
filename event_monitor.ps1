# Monitors the event log fromn the console
param([string]$logfile = "", [string]$server = "",  [int]$severity = 4, [string]$filter = "")

function msg_ok
{
	 Write-Host
	 Write-Host "  v $args" -ForegroundColor "Green"
}

function msg_crit
{
	 Write-Host
	 Write-Host "  × $args" -ForegroundColor "Red"
}

function msg_info
{
	 Write-Host
	 Write-Host "  i $args" -ForegroundColor "Cyan"
}

function msg_warn
{
	 Write-Host
	 Write-Host "  ? $args" -ForegroundColor "Yellow"
}

function msg_text
{
	 Write-Host " $args"
}

msg_ok "Real Time Event Monitor v1.0 by Patrick Lambert - http://dendory.net"
if(!$logfile)
{
	 msg_warn "Usage: event_monitor -logfile <log file> [-server <remote host>] [-filter <{event IDs}>] [-severity <1..4>]"
	 msg_text ""
	 $logfile = Read-Host "Log file (Default: Application)"
	 if($logfile -eq "")
	 {
		 $logfile = "Application"
	 }
	 $server = Read-Host " System address (Default: localhost)"
	 $filter = Read-Host " Entry IDs to monitor (Default: All)"
	 $severity = Read-Host "    Lowest severity to show [1..4] (Default: 4)"
	 if($severity -eq "")
	 {
		 $severity = 4;
	 }
}

$date = (Get-Date (Get-Date -Format d)).AddYears(-1)
msg_text "Fetching logs..."

DO
{
	 try {
	 if($server -ne "")      # This is crazy, all because PowerShell always assumes a string is a single argument...
	 {
		 if($filter -ne "")
		 {
			  $logs = Get-EventLog $logfile -After $date -ComputerName $server -InstanceId $filter -ErrorAction Stop | Sort-Object index | Select -last 30
		 }
		 else
		 {
			  $logs = Get-EventLog $logfile -After $date -ComputerName $server -ErrorAction Stop | Sort-Object index | Select -last 30
		 }
	 }
	 else
	 {
		 if($filter -ne "")
		 {
			  $logs = Get-EventLog $logfile -After $date -InstanceId $filter -ErrorAction Stop | Sort-Object index | Select -last 30
		 }
		 else
		 {
			  $logs = Get-EventLog $logfile -After $date -ErrorAction Stop | Sort-Object index | Select -last 30
		 }
	 }
	 } catch [System.ArgumentException] { } 
	 Foreach($log in $logs)
	 {
		 $type = $log.EntryType
		 $id = $log.InstanceId
		 $src = $log.Source
		 $gen = $log.TimeGenerated
		 $message = $log.Message
		 $message = $message -replace '\r|\n', " "
		 if($type -eq "Information" -and $severity -gt 2)
		 {
			  msg_info "[$id] $src - $gen"
			  msg_text $message.Substring(0, [System.Math]::Min(100, $message.Length)) "..."
		 }
		 elseif($type -eq "Warning" -and $severity -gt 1)
		 {
			  msg_warn "[$id] $src - $gen"
			  msg_text $message.Substring(0, [System.Math]::Min(100, $message.Length)) "..."
		 }
		 elseif($type -eq "Error" -or $type -eq "Critical")
		 {
			  msg_crit "[$id] $src - $gen"
			  msg_text $message.Substring(0, [System.Math]::Min(100, $message.Length)) "..."
		 }
		 elseif($severity -gt 3)
		 {
			  msg_ok "[$id] $src - $gen"
			  msg_text $message.Substring(0, [System.Math]::Min(100, $message.Length)) "..."
		 }
		 $date = $log.TimeWritten
	 }
	 Start-Sleep -s 5
} While(1)

 
