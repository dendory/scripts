function Read-InputBox
{
   <#
    .SYNOPSIS
        Read-InputBox creates a visual input box and waits for user input.

    .DESCRIPTION
        The Read-InputBox function creates a Windows Forms dialog box with custom text and awaits user input. The dialog box can be customized with various parameters. The text entered is then returned to the user.
   
    .EXAMPLE
        $input = Read-InputBox -Text "Enter your email address" -Title "Email" -Default "test@example.com"

        Create an input box with a custom text label, title and entry value, then place the result in $input.

    .LINK
        Author: Patrick Lambert - http://dendory.net
    #>


    param([string]$Text = "Enter your input:", [string]$Title = "Input", [string]$Default = "")

    # Import assembly
    Add-Type -AssemblyName System.Windows.Forms

    # Create form
    $inputbox = New-Object System.Windows.Forms.Form
    $inputbox.Font = New-Object System.Drawing.Font("Times New Roman", 12)
    $inputbox.AutoSize = $false
    $inputbox.Width = 450
    $inputbox.Height = 200
    $inputbox.AutoSizeMode = "GrowAndShrink"
    $inputbox.StartPosition = "CenterScreen"
    $inputbox.FormBorderStyle = "FixedSingle"
    $inputbox.Text = $Title

    # Create label
    $inputlabel = New-Object System.Windows.Forms.Label
    $inputlabel.AutoSize = $false
    $inputlabel.Left = 20
    $inputlabel.Top = 10
    $inputlabel.Width = 400
    $inputlabel.Height = 60
    $inputlabel.TextAlign = "MiddleLeft"
    $inputlabel.Text = $Text

    # Create entry
    $inputentry = New-Object System.Windows.Forms.TextBox
    $inputentry.AutoSize = $true
    $inputentry.Text = $Default
    $inputentry.Left = 20
    $inputentry.Top = 80
    $inputentry.Width = 400

    # Create button
    $inputbutton = New-Object System.Windows.Forms.Button
    $inputbutton.AutoSize = $true
    $inputbutton.Top = 120
    $inputbutton.Left =345
    $inputbutton.Text = "Ok"
    $inputbutton.Add_Click({$inputbox.Close()})

    # Display controls
    $inputbox.Controls.Add($inputlabel)
    $inputbox.Controls.Add($inputentry)
    $inputbox.Controls.Add($inputbutton)
    $inputbox.ShowDialog() | Out-Null

    return $inputentry.Text
}

Export-ModuleMember Read-InputBox
