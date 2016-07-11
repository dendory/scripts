$pass = ConvertTo-SecureString "P@ssW0rD!" -AsPlainText -Force
$fqdn = "EXAMPLE.COM"
$ou = "OU=Users,DC=example,DC=com"
$numberofusers = 100

for($i=0; $i -lt $numberofusers; $i++)
{
    $data = Invoke-WebRequest -Uri "https://randomuser.me/api/"
    $user = $data.Content | ConvertFrom-Json
    $email = $user.results[0].user.email -replace '\s',''
    $upn = "$($user.results[0].user.username)@$fqdn"
    New-ADUser $user.results[0].user.username -AccountPassword $pass -ChangePasswordAtLogon $false -PostalCode $user.results[0].user.location.zip -Country $user.nationality -State $user.results[0].user.location.state -City $user.results[0].user.location.city -StreetAddress $user.results[0].user.location.street -GivenName $user.results[0].user.name.first -Surname $user.results[0].user.name.last -DisplayName "$($user.results[0].user.name.first) $($user.results[0].user.name.last)" -EmailAddress $email -OfficePhone $user.results[0].user.phone -Enabled $true -EmployeeID $user.results[0].user.dob -UserPrincipalName $upn -Path $ou
}
