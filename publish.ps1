# Windows PowerShell publishing helper for a manually-created empty GitHub repository.
# It does not create, overwrite, delete, or force-push a GitHub repository.
param(
  [string]$Repository = 'https://github.com/Unsull/asm-handbook-th.git'
)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw 'Git is not installed or not in PATH. Install Git for Windows first.'
}
if (-not (Test-Path './package.json')) {
  throw 'Run this script from the extracted asm-handbook-th project folder.'
}
Write-Host 'Repository:' $Repository
Write-Host 'Make sure you already created an EMPTY repository on GitHub.'

if (-not (Test-Path './.git')) {
  git init -b main
  if ($LASTEXITCODE -ne 0) { throw 'git init failed' }
}

$branch = (git branch --show-current).Trim()
if ($branch -ne 'main') {
  throw "Current Git branch is '$branch'. This helper only publishes branch 'main'."
}

$remotes = @(git remote)
if ($remotes -contains 'origin') {
  $existing = (git remote get-url origin).Trim()
  if ($existing -ne $Repository) {
    throw "Existing origin is '$existing' rather than '$Repository'. Resolve manually; no remote was modified."
  }
} else {
  git remote add origin $Repository
  if ($LASTEXITCODE -ne 0) { throw 'Adding origin remote failed' }
}

git add .
if ($LASTEXITCODE -ne 0) { throw 'git add failed' }
$staged = @(git diff --cached --name-only)
if ($staged.Count -gt 0) {
  git commit -m 'Initial release: Thai ASM handbook'
  if ($LASTEXITCODE -ne 0) { throw 'git commit failed. Check git user.name and user.email.' }
} else {
  Write-Host 'No staged changes to commit.'
}

git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'git push failed. Verify the GitHub repository exists and authentication is configured.' }
Write-Host 'Push completed. Open GitHub Settings > Pages and select GitHub Actions as Source.'
