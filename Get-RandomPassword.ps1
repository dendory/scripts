# Created by: Patrick Lambert - http://dendory.net
#
# This script creates a random password including upper case letters, lower case letters, numbers, and optionally complex characters.
# Usage:
#
# Get-RandomPassword -Length 12 -Complex
#
Function Get-RandomPassword([int32]$Length = 8, [Switch]$Complex)
{
    $chars = @("abcdefghijkmnopqrstuvwxyz", "ABCEFGHJKLMNPQRSTUVWXYZ", "1234567890", "!@#$%^&*()-+")
    Do 
    {
        $result = ""
        for($i = 0; $i -lt $Length; $i++)
        {
            if($Complex) { $j = Get-Random -Maximum 4 }
            else { $j = Get-Random -Maximum 3 }
            $result += $chars[$j][(Get-Random -Maximum $chars[$j].Length)]
        }
    } Until($result -cmatch “[A-Z]” -and $result -cmatch “[a-z]” -and $result -cmatch “[0-9]” -and (!$Complex -or $result -cmatch “[\!\@\#\$\%\^\&\*\(\)\-\+]”) -or ($Length -lt 4 -or (!$Complex -and $Length -lt 3)))
    $result
}