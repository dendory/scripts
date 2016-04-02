function Get-GeoIP([Parameter(Mandatory=$true)][string]$IP)
{
   <#
    .SYNOPSIS
        Get-GeoIP returns the country of an IP address

    .DESCRIPTION
        Each IP block is assigned to a specific organization. This function queries the webservicex.net API to retrieve the last known country for a specific IP.
 
    .EXAMPLE
        Get-GeoIP -IP 192.168.0.1

        Get the country information for a specific IP.

    .EXAMPLE
        Get-GeoIP 8.8.8.8 | Select CountryCode

        Show only the country code for a specific IP.

    .LINK
        Author: Patrick Lambert - http://dendory.net
    #>
    $geoip = New-WebServiceProxy -Uri "http://www.webservicex.net/geoipservice.asmx?wsdl" -Namespace WebServiceProxy
    $geoip.GetGeoIP($IP)
}

Export-ModuleMember Get-GeoIP