param([string]$Output = "share_report.html")

"<html>
<body>
<style>
html, body
{
font-family: tahoma, arial;
font-size: 14px;
margin: 5px;
padding: 0px;
color: #2E1E2E;
}
table
{
border-collapse: collapse;
    width: 100%;
}
th
{
border: 1px solid #8899AA;
padding: 3px 7px 2px 7px;
font-size: 1.1em;
text-align: left;
padding-top: 5px;
padding-bottom: 4px;
background-color: #AABBCC;
color: #ffffff;
}
td
{
border: 1px solid #8899AA;
padding: 3px 7px 2px 7px;
    overflow: hidden;
}
h2
{
    text-align: center;
font-size: 22px;
    text-shadow: 1px 1px 1px rgba(150, 150, 150, 0.5);
}
</style>" > $Output

"<h2>GROUP MEMBERS</h2><table>" >> $Output

$groups = Get-ADGroup -Filter * -Properties *
foreach($g in $groups) 
{ 
    if($g.members) 
    { 
        "<tr><th>$($g.name)</th></tr><tr><td>" >> $Output
        foreach ($member in $g.members) { "$member<br>" >> $Output }
        "</td></tr>" >> $Output
    }
}

"</table><h2>SHARE PERMISSIONS</h2>" >> $Output
$shares = Get-WmiObject win32_LogicalShareSecuritySetting | select -ExpandProperty name
foreach($share in $shares)
{
    "<table><tr><th colspan=2>$share</th></tr>" >> $Output
    $descr = Get-WmiObject win32_LogicalShareSecuritySetting | Where { $_.name -eq $share }
    $acls = $descr.GetSecurityDescriptor().Descriptor.DACL
    foreach($acl in $acls)
    {
        "<tr><td>$($acl.Trustee.Domain)\$($acl.Trustee.Name)</td><td>$($acl.AccessMask -Replace 2032127,"Full Control" -Replace 1245631,"Change" -Replace 1179817,"Read")</td></tr>" >> $Output
    }
    "</table>" >> $Output
}
"</body></html>" >> $Output

Write-Host "Report saved to: $Output"
