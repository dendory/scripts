function Test-Uptime
{
   <#
    .SYNOPSIS
        Test-Uptime tests connectivity to a list of hosts

    .DESCRIPTION
        Use Test-Uptime to compile a list of hosts and test connectivity. Run it on a schedule and view the last time your hosts were last up. The list of hosts is stored in a CSV file, and results are updated in that file each time the function is run. The default CSV is ".\lastonline.csv"
        
        From this function you can add hosts, remove hosts, run the tests, and show the results.
   
    .EXAMPLE
        Test-Uptime -Add "1.2.3.4"

        Add a host to your list of monitored hosts.

    .EXAMPLE
        Test-Uptime -Remove "1.2.3.4"

        Remove a host to your list of monitored hosts.

    .EXAMPLE
        Test-Uptime

        Run connectivity tests on your list of monitored hosts.

    .EXAMPLE
        Test-Uptime -Quiet -CsvFile "C:\temp\file.csv"

        Run tests on your monitored hosts by reading a specific CSV file, and don't print results at the end.

    .EXAMPLE
        Test-Uptime -ShowResults

        Show the last connectivity results without running tests.

    .LINK
        Author: Patrick Lambert - http://dendory.net
    #>
    param([switch]$Quiet, [switch]$ShowResults, [string]$Add = "", [string]$Remove = "", [string]$CsvFile = ".\lastonline.csv")

    $csv = Get-Content $CsvFile -ErrorAction SilentlyContinue | ConvertFrom-Csv
    $results = @()
    if($Add -ne "")   # Add an entry to the file
    {
        if($csv) { $results += $csv }
        $results += New-Object PSObject -Property @{ Hostname = $Add; LastOnline = "Never" }
        $results | ConvertTo-Csv | Out-File $CsvFile
    }
    elseif($Remove -ne "")   # Remove an entry from the file
    {
        foreach($line in $csv)
        {
            if($line.Hostname -ne $Remove) { $results += New-Object PSObject -Property @{ Hostname = $line.Hostname; LastOnline = $line.LastOnline } }
            $results | ConvertTo-Csv | Out-File $CsvFile
        }
    }
    elseif(!$ShowResults)   # Run the tests and update the file
    {
        $i = 0;
        foreach($line in $csv)
        {
            if($line.Hostname)
            {
                write-progress -activity "Testing hosts:" -status $line.Hostname -percentcomplete ($i++ / $csv.count * 100)
                if(Test-Connection -ComputerName $line.Hostname -BufferSize 16 -Count 1 -ea 0 -quiet)
                {
                    $results += New-Object PSObject -Property @{ Hostname = $line.Hostname; LastOnline = (Get-Date) }
                }
                else
                {
                    $results += New-Object PSObject -Property @{ Hostname = $line.Hostname; LastOnline = $line.LastOnline }
                }
            }
        }
        $results | ConvertTo-Csv | Out-File $CsvFile
        if(!$Quiet) { $results }
    }
    else   # Just show the last results
    {
        $csv
    }
}

Export-ModuleMember Test-Uptime
