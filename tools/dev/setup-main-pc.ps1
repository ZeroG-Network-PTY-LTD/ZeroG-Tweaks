<#
ZeroG-Tweaks dev setup for a new Windows PC. Safe to run again: every step checks first and skips what is done.

  1. checks git, GitHub CLI, Python 3 and Java 21 (prints the winget command for anything missing)
  2. git identity for ZeroG repos only: MrWhiteFlamesYT <popmaster124@gmail.com> (other repos keep your normal name)
  3. GitHub CLI signed in and switched to the ZeroG-Network account, used by git for pushes
  4. clones ZeroG-Tweaks (branch 1.21.x) to -Path, or updates it if it is already there;
     optional -Design adds the Design branch as a second folder next to it
  5. Python package nbtlib (structure templates)
  6. run-server/ with RCON on (random password) for tools/dev/rcon.py; you accept the Minecraft EULA yourself

Run in PowerShell (from a downloaded copy of this file, or from tools\dev in a clone):
  powershell -ExecutionPolicy Bypass -File setup-main-pc.ps1 -Path "$HOME\Desktop\claude\ZeroG-Tweaks" -Design
#>
param(
    [string]$Path = "$HOME\Desktop\claude\ZeroG-Tweaks",
    [switch]$Design
)
$ErrorActionPreference = 'Continue'   # git/gh print progress on stderr; failures are checked below
$Repo = 'https://github.com/ZeroG-Network-PTY-LTD/ZeroG-Tweaks'
$GhAccount = 'ZeroG-Network'
$missing = @()

function Step($text) { Write-Host ""; Write-Host "== $text" -ForegroundColor Cyan }
function Have($cmd) { return [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

# ---- 1. tools ------------------------------------------------------------------------------------------------------------
Step 'Checking tools'
if (-not (Have git))    { $missing += 'winget install --id Git.Git -e' }
if (-not (Have gh))     { $missing += 'winget install --id GitHub.cli -e' }
$py = $null
foreach ($c in @('python', 'py')) { if ((-not $py) -and (Have $c)) { $py = $c } }
if (-not $py)           { $missing += 'winget install --id Python.Python.3.12 -e' }
$javaOk = $false
$javaCandidates = @()
if ($env:JAVA_HOME) { $javaCandidates += (Join-Path $env:JAVA_HOME 'bin\java.exe') }
if (Have java) { $javaCandidates += (Get-Command java).Source }
foreach ($j in ($javaCandidates | Select-Object -Unique)) {
    if (Test-Path $j) {
        $v = (& cmd /c "`"$j`" -version 2>&1") -join ' '
        if ($v -match 'version "21') { $javaOk = $true; Write-Host "Java 21: $j" }
    }
}
if (-not $javaOk)       { $missing += 'winget install --id EclipseAdoptium.Temurin.21.JDK -e   (then open a new PowerShell)' }
if ($missing.Count -gt 0) {
    Write-Host 'Missing - install these, open a new PowerShell window, and run this script again:' -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host "  $_" }
    exit 1
}
Write-Host 'git, gh, python and Java 21 found.'

# ---- 2. git identity for ZeroG repos ------------------------------------------------------------------------------------
Step 'Git identity for ZeroG repos'
$zerogConfig = Join-Path $HOME '.gitconfig-zerog'
git config --file $zerogConfig user.name 'MrWhiteFlamesYT'
git config --file $zerogConfig user.email 'popmaster124@gmail.com'
$includes = @(& cmd /c 'git config --global --get-regexp ^^includeif\. 2>nul')
foreach ($pattern in @('hasconfig:remote.*.url:https://github.com/ZeroG-Network-PTY-LTD/**',
                       'hasconfig:remote.*.url:git@github.com:ZeroG-Network-PTY-LTD/**')) {
    if (-not ($includes -match [regex]::Escape($pattern))) {
        git config --global --add "includeIf.$pattern.path" '~/.gitconfig-zerog'
    }
}
Write-Host 'Commits in ZeroG-Network-PTY-LTD repos will show MrWhiteFlamesYT.'

# ---- 3. GitHub CLI account -----------------------------------------------------------------------------------------------
Step "GitHub CLI account ($GhAccount)"
$status = (& cmd /c 'gh auth status 2>&1') -join "`n"
if ($status -notmatch "account $GhAccount") {
    Write-Host "Sign in as $GhAccount in the browser window that opens."
    gh auth login --hostname github.com --git-protocol https --web
}
& cmd /c "gh auth switch --hostname github.com --user $GhAccount 2>nul" | Out-Null
gh auth setup-git
$status = (& cmd /c 'gh auth status 2>&1') -join "`n"
if ($status -notmatch "account $GhAccount[^\n]*\n[^\n]*Active account: true") {
    Write-Host "Warning: $GhAccount is not the active gh account. Run: gh auth switch --user $GhAccount" -ForegroundColor Yellow
} else { Write-Host "$GhAccount is active." }

# ---- 4. clone or update --------------------------------------------------------------------------------------------------
Step "Repository at $Path"
if (Test-Path (Join-Path $Path '.git')) {
    git -C $Path fetch --all --prune
    $branch = (git -C $Path rev-parse --abbrev-ref HEAD).Trim()
    if ($branch -eq '1.21.x') { git -C $Path pull --ff-only } else { Write-Host "On branch $branch - not pulling." }
} else {
    New-Item -ItemType Directory -Force (Split-Path $Path) | Out-Null
    git clone --branch 1.21.x $Repo $Path
    if ($LASTEXITCODE -ne 0) { Write-Host 'Clone failed - check the gh sign-in above.' -ForegroundColor Red; exit 1 }
}
Write-Host ("Commit identity here: " + (git -C $Path config user.name) + " <" + (git -C $Path config user.email) + ">")
if ($Design) {
    $designPath = "$Path-Design"
    if (-not (Test-Path $designPath)) {
        git -C $Path fetch origin Design
        git -C $Path worktree add $designPath Design
    } else { git -C $designPath pull --ff-only }
    Write-Host "Design branch: $designPath"
}

# ---- 5. python packages --------------------------------------------------------------------------------------------------
Step 'Python packages'
& $py -m pip install --quiet --disable-pip-version-check --upgrade nbtlib
Write-Host 'nbtlib installed.'

# ---- 6. dev server with RCON ---------------------------------------------------------------------------------------------
Step 'Dev server (run-server) with RCON'
$server = Join-Path $Path 'run-server'
New-Item -ItemType Directory -Force $server | Out-Null
$propsFile = Join-Path $server 'server.properties'
$props = [ordered]@{}
if (Test-Path $propsFile) {
    foreach ($line in Get-Content $propsFile) {
        if ($line -match '^([^#=]+)=(.*)$') { $props[$Matches[1]] = $Matches[2] }
    }
}
if (-not $props['rcon.password']) {
    $bytes = New-Object byte[] 12
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $props['rcon.password'] = -join ($bytes | ForEach-Object { $_.ToString('x2') })
}
$props['enable-rcon'] = 'true'
if (-not $props['rcon.port']) { $props['rcon.port'] = '25575' }
if (-not $props['online-mode']) { $props['online-mode'] = 'false' }
$lines = $props.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }
[System.IO.File]::WriteAllLines($propsFile, [string[]]$lines)   # no BOM: Minecraft reads it as plain text
Write-Host 'RCON is on (password kept in run-server\server.properties, which git ignores).'
$eula = Join-Path $server 'eula.txt'
if (-not ((Test-Path $eula) -and ((Get-Content $eula -Raw) -match 'eula=true'))) {
    Write-Host 'The dev server needs the Minecraft EULA: https://aka.ms/MinecraftEULA'
    $answer = Read-Host 'Type yes if you accept it (anything else skips; you can do this later)'
    if ($answer -eq 'yes') { [System.IO.File]::WriteAllText($eula, "eula=true`n") }
}

Step 'Done'
Write-Host "Project:      $Path"
Write-Host 'Play/test:    .\gradlew.bat runClient'
Write-Host 'Dev server:   .\gradlew.bat runServer      then  python tools\dev\rcon.py "list"'
Write-Host 'Game tests:   .\gradlew.bat runZeroGTests -PzeroGTests -PtidewraithTests'
Write-Host 'Tools:        tools\dev\README.md'
