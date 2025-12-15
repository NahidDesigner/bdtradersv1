#!/bin/bash
# Script to upload BD Tenant SaaS Platform to GitHub using Git Bash

echo "🚀 Uploading BD Tenant SaaS Platform to GitHub..."
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not in PATH. Trying to find Git Bash..."
    # Try common Git installation paths
    if [ -f "/c/Program Files/Git/bin/git.exe" ]; then
        export PATH="/c/Program Files/Git/bin:$PATH"
    elif [ -f "/c/Program Files (x86)/Git/bin/git.exe" ]; then
        export PATH="/c/Program Files (x86)/Git/bin:$PATH"
    else
        echo "❌ Could not find Git. Please add Git to your PATH or run this from Git Bash."
        exit 1
    fi
fi

echo "✅ Git found: $(git --version)"
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files..."
git add .

# Check if there are changes
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Creating commit..."
    git commit -m "Initial commit: BD Tenant SaaS Platform - Multi-tenant platform for Bangladesh merchants

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
- Coolify-ready deployment"
fi

# Check if remote exists
if git remote get-url origin &> /dev/null; then
    echo "🔄 Remote already exists, updating..."
    git remote set-url origin https://github.com/NahidDesigner/bdtradersv1.git
else
    echo "➕ Adding remote repository..."
    git remote add origin https://github.com/NahidDesigner/bdtradersv1.git
fi

# Set main branch
git branch -M main

echo ""
echo "⬆️  Pushing to GitHub..."
echo "⚠️  You will be prompted for credentials:"
echo "   - Username: Your GitHub username"
echo "   - Password: Use a Personal Access Token (not your password)"
echo "   - Create token: https://github.com/settings/tokens"
echo ""

# Push to GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your code is now on GitHub!"
    echo "🔗 Repository: https://github.com/NahidDesigner/bdtradersv1"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. You have access to the repository"
    echo "   2. You're using a Personal Access Token"
    echo "   3. The repository exists on GitHub"
fi

