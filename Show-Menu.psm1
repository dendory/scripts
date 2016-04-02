# (C) 2015 Patrick Lambert - http://dendory.net - Provided under the MIT License.
#
# Usage:
#  Import-Module .\Show-Menu.psm1
#  Show-Menu -Title "This is a test of the menu system" -MenuOptions @("The first choice", "The good choice", "The last choice")
#

function Center-Text([Parameter(Mandatory=$true)][string][string]$Message, [string]$Color = "gray", [bool]$NoEOL = $false)
{
    $offset = [Math]::Round(([Console]::WindowWidth / 2) + ($Message.Length / 2))
    if($NoEOL) { Write-Host ("{0,$offset}" -f $Message) -ForegroundColor $Color -NoNewline }
    else { Write-Host ("{0,$offset}" -f $Message) -ForegroundColor $Color }
}

function Show-Menu([Parameter(Mandatory=$true)][string]$Title, [string]$SubTitle = "Please select an option from the following choices", [string]$Prompt = "Your choice: ", [Parameter(Mandatory=$true)][string[]]$MenuOptions, [string[]]$NonMenuOptions)
{
   <#
    .SYNOPSIS
        Show-Menu creates a colorful menu on the screen.

    .DESCRIPTION
        Use this function to display a color menu on the console screen. It can display a number of menu items and await a choice, returning this choice. Optionally, it can also display some non-menu options.
   
    .EXAMPLE
        Show-Menu -Title "This is a test of the menu system" -MenuOptions @("The first choice", "The good choice", "The last choice")

        Show a menu with three choices.

    .LINK
        Author: Patrick Lambert - http://dendory.net    
    #>
    $result = 99
    while($result -gt $i -or $result -lt 1)
    {
        $i = 0
        cls
        Write-Host
        Center-Text -Message $Title -Color "Magenta"
        Write-Host
        Center-Text -Message $SubTitle -Color "Cyan"
        Write-Host
        foreach($opt in $NonMenuOptions)
        {
		    Write-Host "`t$opt" -ForegroundColor Cyan
	    }
        foreach($opt in $MenuOptions)
        {
            $i++
		    Write-Host "`t$i. $opt" -ForegroundColor Cyan
	    }
        Write-Host
        Center-Text -Message $Prompt -Color "Cyan" -NoEOL $true
        [int]$result = Read-Host
    }
    return $result
}

Export-ModuleMember Show-Menu
