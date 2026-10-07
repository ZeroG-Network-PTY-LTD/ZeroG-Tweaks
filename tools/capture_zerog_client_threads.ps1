param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$instance = 'C:\Users\jakem\curseforge\minecraft\Instances\ZeroG'
$jcmd = 'C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot\bin\jcmd.exe'
# Never print the command line: the launcher may pass account credentials there.
$clients = @(Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -eq 'javaw.exe' -or $_.Name -eq 'java.exe') -and
    $_.CommandLine -and $_.CommandLine.Contains($instance) -and
    $_.CommandLine.Contains('--gameDir')
})
if ($clients.Count -ne 1) { throw "Expected exactly one ZeroG client, found $($clients.Count). No process changed." }
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$clientId = $clients[0].ProcessId
for ($sample=1; $sample -le 2; $sample++) {
    & $jcmd $clientId Thread.print -l | Out-File -Encoding utf8 -FilePath (Join-Path $OutputDirectory "client-threads-$sample.txt")
    if ($LASTEXITCODE -ne 0) { throw 'Thread capture failed. No process changed.' }
    if ($sample -eq 1) { Start-Sleep -Seconds 5 }
}
Write-Output 'Two scoped client thread samples captured. No process stopped and no save modified.'
