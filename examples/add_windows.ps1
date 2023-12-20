# NOTES, this script is untested. Honestly, I asked ChatGPT to convert the bash script that I was using to Powershell.
# Check if both team name and API key are provided
param(
    [Parameter(Mandatory=$true)]
    [string]$teamname,

    [Parameter(Mandatory=$true)]
    [string]$apiKey
)

$url = "https://nodeboard.io/a/$teamname/n/api/managedsites/"

# Gather system information
$hostname = $env:COMPUTERNAME
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -eq 'Wi-Fi' } | Select-Object -First 1).IPAddress
$osType = (Get-WmiObject Win32_OperatingSystem).Caption
$kernelVersion = (Get-WmiObject Win32_OperatingSystem).Version
$serialNumber = (Get-WmiObject Win32_BIOS).SerialNumber
$ram = [math]::Round(((Get-WmiObject Win32_ComputerSystem).TotalPhysicalMemory / 1GB), 2)
$cpuType = (Get-WmiObject Win32_Processor).Name
$cpuCores = (Get-WmiObject Win32_Processor).NumberOfCores
$uptime = (Get-Uptime).ToString()

# JSON data to be sent in the POST request
$dataJson = @{
    name = $hostname
    url = "http://example.com"
    ip_address = $ipAddress
    notes = "Zbook 15 G3"
    description = "Laptop"
    tags = @($osType, $kernelVersion, "OS Version: $osVersion", "Serial: $serialNumber", "RAM: $ram GB", "CPU: $cpuType", "Cores: $cpuCores", "Uptime: $uptime")
} | ConvertTo-Json

# POST request with Invoke-WebRequest
try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers @{Authorization = "Api-Key $apiKey"} -ContentType "application/json" -Body $dataJson
    Write-Host "Data successfully sent to Nodeboard."
} catch {
    Write-Host "Error: Failed to send data to Nodeboard. Response code: $($_.Exception.Response.StatusCode.Value__)"
    exit 1
}
