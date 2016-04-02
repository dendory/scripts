Function Show-Chart
{
   <#
    .SYNOPSIS
        Show-Chart draws a chart

    .DESCRIPTION
        With Show-Chart you can create a chart on the screen and optionally save it to a file. It uses the Windows Forms control to create the chart, then can be controlled using various parameters. See the examples for details.
  
    .EXAMPLE
        Show-Chart

        Draw a chart using the default dataset (top 5 running processes sorted based on memory usage), default width, height and column type.

    .EXAMPLE
        Show-Chart -Title "Food calories" -Dataset @{"Muffin" = 377; "Apple" = 52; "Banana" = 89} -Type "Point"

        Draw a point chart with a custom title and dataset.

    .EXAMPLE
        Show-Chart -Width 800 -Height 800 -Output chart.png

        Draw a default chart with the specified resolution, but do not display it, save it directly to a file (format must be PNG).

    .EXAMPLE
        Show-Chart -Type "Pie" -Dataset $set -ShowValues $false

        Draw a pie chart with a custom data set, and do not show individual values on the chart.

    .LINK
        Author: Patrick Lambert - http://dendory.net
    #>
    param([string]$Title = "", [string]$Output = "", $Dataset = @{}, [int32]$Width = 700, [int32]$Height = 500, [string]$Type = "Column", [boolean]$ShowValues = $true)

    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Windows.Forms.DataVisualization
    $chart = New-object System.Windows.Forms.DataVisualization.Charting.Chart
    $chart.Width = $Width
    $chart.Height = $Height
    $chart.Top = 50
    $chart.Left = 50
    $chartarea = New-Object System.Windows.Forms.DataVisualization.Charting.ChartArea
    $chartarea.BackColor = "#FFFFFF"
    $chartarea.BackSecondaryColor = "#FFFFFF"
    $chartarea.BackGradientStyle = "DiagonalRight"
    if($Dataset.Count -eq 0)
    {
        $Title = "Top 5 memory usage processes (MB)"
        Get-Process | Sort -Property WorkingSet | Select ProcessName,@{Name='Memory';Expression={[math]::Round($_.WorkingSet / 1000000,1)}} -Last 5 | Foreach { $Dataset[$_.ProcessName] = [double]$_.Memory }
    }
    $chart.ChartAreas.Add($chartarea)
    $chart.Titles.Add($Title) | Out-Null
    $chart.Titles[0].Font = New-Object System.Drawing.Font("Times New Roman", 16)
    $chart.Series.Add("dataset") | Out-Null
    $chart.Series[0].Points.DataBindXY($Dataset.Keys, $Dataset.Values)
    $chart.Series[0].ChartType = [System.Windows.Forms.DataVisualization.Charting.SeriesChartType]::$Type
    $chart.Series[0].IsValueShownAsLabel = $ShowValues
    $chart.Series[0]["PieLabelStyle"] = "Outside"
    $chart.Series[0]["DrawingStyle"] = "Emboss"
    $chart.Series[0]["PieLineColor"] = "Black"
    $chart.Series[0]["PieDrawingStyle"] = "Concave"
    $chart.Anchor = [System.Windows.Forms.AnchorStyles]::Bottom -bor [System.Windows.Forms.AnchorStyles]::Left -bor [System.Windows.Forms.AnchorStyles]::Right -bor [System.Windows.Forms.AnchorStyles]::Top
    $form = New-Object Windows.Forms.Form
    $form.Width = $Width + 100
    $form.Height = $Height + 120
    $form.Controls.Add($chart)
    $save = New-Object Windows.Forms.Button
    $save.Text = "Save Chart"
    $save.Top = 10
    $save.Left = 10
    $save.Width = 100
    $save.Anchor = [System.Windows.Forms.AnchorStyles]::Top -bor [System.Windows.Forms.AnchorStyles]::Left
    $save.add_click({
        $browse = New-Object System.Windows.Forms.SaveFileDialog
        $browse.initialDirectory = $Env:USERPROFILE + "\Desktop\"
        $browse.filter = "Images (*.png)| *.png"
        $browse.filename = "chart.png"
        $browse.ShowDialog() | Out-Null
        $browse.FilterIndex
        $chart.SaveImage($browse.filename, "PNG")
        $label.Text = "Saved to: " + $browse.filename 
    })
    $form.controls.add($save)
    $label = New-Object Windows.Forms.Label
    $label.Top = 15
    $label.Left = 120
    $label.Width = $Width - 150
    $form.controls.add($label)
    if($Output -eq "")
    {
        $form.ShowDialog() | Out-Null
    }
    else
    {
        $chart.SaveImage($Output, "PNG")
    }
}

Export-ModuleMember Show-Chart
