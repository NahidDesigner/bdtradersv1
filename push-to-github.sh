#!/bin/bash

# Script to push BD Tenant SaaS Platform to GitHub
# Repository: https://github.com/NahidDesigner/bdtradersv1.git

echo "🚀 Pushing BD Tenant SaaS Platform to GitHub..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo "📝 Adding files..."
git add .

# Create commit
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

# Check if remote exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "🔄 Remote already exists, updating..."
    git remote set-url origin https://github.com/NahidDesigner/bdtradersv1.git
else
    echo "➕ Adding remote repository..."
    git remote add origin https://github.com/NahidDesigner/bdtradersv1.git
fi

# Set main branch
git branch -M main

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git push -u origin main

echo "✅ Done! Your code is now on GitHub."
echo "🔗 Repository: https://github.com/NahidDesigner/bdtradersv1"

