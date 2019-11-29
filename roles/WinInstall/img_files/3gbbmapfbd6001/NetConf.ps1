# DOMAIN STUFF

# DOMAIN MUST BE "national.core.bbc.co.uk"
$domain = "national.core.bbc.co.uk"
#USERNAME MUST BE "national.core.bbc.co.uk\ERE_ACCOUNT_LOGIN_HERE"
$username = "national.core.bbc.co.uk\ere-mid-tf" 
#MUST BE ERE ACCOUNT PASSWORD HERE
$password = "W@shed5ocks!" | ConvertTo-SecureString -asPlainText -Force


# NIC 1
$ip1 = "10.72.127.120"
$gateway1 = "10.72.127.254"
#$netmask1 = "255.255.255.0"
$dns1_1 = "10.72.136.53"
$dns2_1 = "10.72.136.4"
#For VMs this is "Ethernet0", for actual machines this is usually "Local Area Connection"
$adapter_alias1 = "Ethernet0"

# NIC 2
#$ip2 = 
#$gateway2 = 
#$netmask2 = 
#$dns1_2 = 
#$dns2_2 = 
#$adapter_alias2 = 
# Raise to ADMIN priviledges
if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }

# Ser NIC 1 Settings
New-NetIPAddress -InterfaceAlias "$adapter_alias1" -IPAddress $ip1 -PrefixLength 24 -DefaultGateway $gateway1
Set-DnsClientServerAddress -InterfaceAlias "$adapter_alias1" -ServerAddresses ("$dns1_1","$dns1_2")

# Wait 10 secs for IP's to take properly...just in case
Start-Sleep -s 10

$credential = New-Object System.Management.Automation.PSCredential($username,$password)
Add-Computer -DomainName $domain -Credential $credential

New-Item D:\InstallComplete.txt -ItemType file

Read-Host -Prompt "Wait for reboot..."
