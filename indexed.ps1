# Search the Windows file system for files modified within the last week using the Windows Search indexer

$con = New-Object -ComObject ADODB.Connection
$rs = New-Object -ComObject ADODB.Recordset
$con.Open("Provider=Search.CollatorDSO;Extended Properties='Application=Windows';")
$rs.Open("SELECT System.ItemPathDisplay, System.DateModified FROM SYSTEMINDEX ORDER BY System.DateModified DESC" , $con)

While(-Not $rs.EOF)
{
	$rs.Fields.Item("System.ItemPathDisplay").Value + " - " + $rs.Fields.Item("System.DateModified").Value
	$rs.MoveNext()
	if($rs.Fields.Item("System.DateModified").Value -lt (Get-Date).AddDays(-7)) { Exit }
}
