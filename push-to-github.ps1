# PowerShell script to push BD Tenant SaaS Platform to GitHub
# Repository: https://github.com/NahidDesigner/bdtradersv1.git

Write-Host "🚀 Pushing BD Tenant SaaS Platform to GitHub..." -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
}

# Add all files
Write-Host "📝 Adding files..." -ForegroundColor Yellow
git add .

# Create commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
$commitMessage = @"
Initial commit: BD Tenant SaaS Platform - Multi-tenant platform for Bangladesh merchants

Features:
- Multi-tenant subdomain-based architecture
- OTP authentication (Bangladesh phone numbers)
- Store and product management
- Order management system
- Shipping classes
- Email & WhatsApp notifications
- Analytics dashboard
- Bangla-first UI with i18n
- PWA support
- Facebook Pixel integration
- Coolify-ready deployment
"@

git commit -m $commitMessage

# Check if remote exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "🔄 Remote already exists, updating..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/NahidDesigner/bdtradersv1.git
} else {
    Write-Host "➕ Adding remote repository..." -ForegroundColor Yellow
    git remote add origin https://github.com/NahidDesigner/bdtradersv1.git
}

# Set main branch
git branch -M main

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "✅ Done! Your code is now on GitHub." -ForegroundColor Green
Write-Host "🔗 Repository: https://github.com/NahidDesigner/bdtradersv1" -ForegroundColor Cyan

