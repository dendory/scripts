function Get-Excuse
{
   <#
    .SYNOPSIS
        Get-Excuse returns an excuse.

    .DESCRIPTION
        This function returns an excuse to be used in a system administration or helpdesk role, based on the BOFH series. The excuses originate from the Bastard Operator From Hell excuse server at http://pages.cs.wisc.edu/~ballard/bofh/ and were modified to fit this module.
  
    .EXAMPLE
        Get-Excuse

        Retrieve one random excuse.

    .LINK
        Author: Patrick Lambert - http://dendory.net
    #>

    [xml]$bofh = Get-Content $PSScriptRoot\bofh.xml
    $bofh.bofh.excuse | Get-Random
}

Export-ModuleMember Get-Excuse
