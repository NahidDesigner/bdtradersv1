# PowerShell script to help install Git and upload to GitHub
# Run this script as Administrator for best results

Write-Host "🚀 BD Tenant SaaS Platform - GitHub Upload Helper" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if Git is installed
$gitInstalled = $false
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        $gitInstalled = $true
        Write-Host "✅ Git is already installed: $gitVersion" -ForegroundColor Green
    }
} catch {
    $gitInstalled = $false
}

if (-not $gitInstalled) {
    Write-Host "❌ Git is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please choose an option:" -ForegroundColor Yellow
    Write-Host "1. Install Git automatically (requires admin)" -ForegroundColor White
    Write-Host "2. Download Git installer" -ForegroundColor White
    Write-Host "3. Use GitHub Desktop instead" -ForegroundColor White
    Write-Host "4. Use GitHub Web Interface" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter your choice (1-4)"
    
    switch ($choice) {
        "1" {
            Write-Host "📥 Downloading Git installer..." -ForegroundColor Yellow
            $gitInstaller = "$env:TEMP\Git-installer.exe"
            Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe" -OutFile $gitInstaller
            Write-Host "✅ Download complete. Please run the installer:" -ForegroundColor Green
            Write-Host "   $gitInstaller" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "After installation, restart PowerShell and run this script again." -ForegroundColor Yellow
            Start-Process $gitInstaller
            exit
        }
        "2" {
            Write-Host "🌐 Opening Git download page..." -ForegroundColor Yellow
            Start-Process "https://git-scm.com/download/win"
            Write-Host "Please download and install Git, then restart PowerShell." -ForegroundColor Yellow
            exit
        }
        "3" {
            Write-Host "🌐 Opening GitHub Desktop download page..." -ForegroundColor Yellow
            Start-Process "https://desktop.github.com/"
            Write-Host "Please download and install GitHub Desktop." -ForegroundColor Yellow
            exit
        }
        "4" {
            Write-Host "🌐 Opening your GitHub repository..." -ForegroundColor Yellow
            Start-Process "https://github.com/NahidDesigner/bdtradersv1"
            Write-Host ""
            Write-Host "Instructions:" -ForegroundColor Cyan
            Write-Host "1. Click 'uploading an existing file' or 'Add file' → 'Upload files'" -ForegroundColor White
            Write-Host "2. Select all files from this folder" -ForegroundColor White
            Write-Host "3. Commit with message: 'Initial commit: BD Tenant SaaS Platform'" -ForegroundColor White
            exit
        }
    }
}

# If Git is installed, proceed with upload
if ($gitInstalled) {
    Write-Host ""
    Write-Host "📦 Preparing to upload to GitHub..." -ForegroundColor Yellow
    Write-Host ""
    
    # Check if already a git repo
    if (-not (Test-Path ".git")) {
        Write-Host "🔧 Initializing git repository..." -ForegroundColor Yellow
        git init
    }
    
    # Add all files
    Write-Host "📝 Adding files..." -ForegroundColor Yellow
    git add .
    
    # Check if there are changes to commit
    $status = git status --porcelain
    if ($status) {
        Write-Host "💾 Creating commit..." -ForegroundColor Yellow
        git commit -m "Initial commit: BD Tenant SaaS Platform - Multi-tenant platform for Bangladesh merchants"
    } else {
        Write-Host "ℹ️  No changes to commit" -ForegroundColor Cyan
    }
    
    # Check if remote exists
    try {
        $remoteExists = git remote get-url origin 2>&1 | Out-Null
        $remoteExists = $true
    } catch {
        $remoteExists = $false
    }
    if ($remoteExists) {
        Write-Host "🔄 Remote already configured: $remoteExists" -ForegroundColor Cyan
        $update = Read-Host "Update remote URL? (y/n)"
        if ($update -eq "y") {
            git remote set-url origin https://github.com/NahidDesigner/bdtradersv1.git
        }
    } else {
        Write-Host "➕ Adding remote repository..." -ForegroundColor Yellow
        git remote add origin https://github.com/NahidDesigner/bdtradersv1.git
    }
    
    # Set main branch
    git branch -M main
    
    Write-Host ""
    Write-Host "⬆️  Ready to push to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  You will need to authenticate:" -ForegroundColor Yellow
    Write-Host "   - Username: Your GitHub username" -ForegroundColor White
    Write-Host "   - Password: Use a Personal Access Token (not your password)" -ForegroundColor White
    Write-Host "   - Create token: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host ""
    
    $push = Read-Host "Push to GitHub now? (y/n)"
    if ($push -eq "y") {
        Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
        git push -u origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✅ Success! Your code is now on GitHub!" -ForegroundColor Green
            Write-Host "🔗 Repository: https://github.com/NahidDesigner/bdtradersv1" -ForegroundColor Cyan
        } else {
            Write-Host ""
            Write-Host "❌ Push failed. Please check:" -ForegroundColor Red
            Write-Host "   1. You have access to the repository" -ForegroundColor White
            Write-Host "   2. You are using a Personal Access Token" -ForegroundColor White
            Write-Host "   3. The repository exists on GitHub" -ForegroundColor White
        }
    } else {
        Write-Host ""
        Write-Host "📋 To push manually, run:" -ForegroundColor Cyan
        Write-Host "   git push -u origin main" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "✨ Done!" -ForegroundColor Green

