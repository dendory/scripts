# This script provisions a new Hyper-V VM on localhost using a template.

$vm_name = Read-Host -Prompt "Enter the new VM name"
$vm_memory = 2GB
$disk_template = "C:\Storage\ISOs\win2012-template.vhdx"
$disk_location = "C:\Users\Public\Documents\Hyper-V\Virtual hard disks"
$switch_name = "New Virtual Switch"

$ErrorActionPreference = "Stop"
copy $disk_template "$disk_location\$vm_name.vhdx"
New-VM -Name "$vm_name" -MemoryStartupBytes $vm_memory -VHDPath "$disk_location\$vm_name.vhdx" -Generation 2 -BootDevice VHD
Connect-VMNetworkAdapter –VMName "$vm_name" -Name "Network Adapter" –SwitchName "$switch_name"
Start-VM "$vm_name"
Get-VMNetworkAdapter "$vm_name" | Select MacAddress
vmconnect localhost "$vm_name"
