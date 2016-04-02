# scripts
Utility scripts made by myself over the years. They are provided under the MIT License

http://dendory.net/

### pushbullet.py
An unofficial pushbullet script to send Pushbullet notifications to all your devices.

Syntax:

    python3 pushbullet.py -key XXXXXXXXXXXXX -title "Test message" -body "This is a test"

### check_ssl.ps1
PowerShell script that retrieves information about a the SSL certificate.

### r53nslookup
This is a PowerShell script that allows you to easily do a DNS lookup on any of your Route 53 Amazon records.

### Test-Uptime.psm1
Use Test-Uptime to compile a list of hosts and test connectivity. Run it on a schedule and view the last time your hosts were last up. The list of hosts is stored in a CSV file, and results are updated in that file each time the function is run. The default CSV is .\lastonline.csv

### Show-Chart.psm1
With Show-Chart you can create a chart on the screen and optionally save it to a file. It uses the Windows Forms control to create the chart, then can be controlled using various parameters. See the examples for details.

### aws_create_instance.ps1
This script will create an EC2 instance, a key pair to connect, add a Route 53 A record for it.

Example:

    .\aws_create_instance.ps1 -AMI ami-d2c924b2 -Subnet subnet-8e3bf3a2 -Type t2.nano -KeyName aws-test -Script c:\scripts\centos_init.sh -Hostname test.example.com -ZoneId Z1W5966G181726

### aws_destroy_instance.ps1

This script will terminate an EC2 instance, delete the attached volumes, remove the A record.

Example:

    .\aws_destroy_instance.ps1 -InstanceId i-XXXXXX -Hostname test.example.com -ZoneId Z1W5966G181726

