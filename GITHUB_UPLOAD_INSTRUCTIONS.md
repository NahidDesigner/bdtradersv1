# 📤 How to Upload to GitHub Repository

Repository: **https://github.com/NahidDesigner/bdtradersv1.git**

## Option 1: Using Git Command Line (Recommended)

### Step 1: Install Git (if not installed)

Download and install Git from: https://git-scm.com/download/win

After installation, restart your terminal/PowerShell.

### Step 2: Open Terminal in Project Directory

Navigate to your project folder:
```powershell
cd "C:\Users\LENOVO\Documents\Cursor apps\Bd tenant"
```

### Step 3: Run These Commands

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create commit
git commit -m "Initial commit: BD Tenant SaaS Platform - Multi-tenant platform for Bangladesh merchants"

# Add remote repository
git remote add origin https://github.com/NahidDesigner/bdtradersv1.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Authenticate

When prompted:
- **Username**: Your GitHub username
- **Password**: Use a **Personal Access Token** (not your GitHub password)
  - Create token: https://github.com/settings/tokens
  - Select scope: `repo` (full control of private repositories)

---

## Option 2: Using GitHub Desktop (Easier)

1. **Download GitHub Desktop**: https://desktop.github.com/
2. **Install and sign in** with your GitHub account
3. **Add Local Repository**:
   - Click "File" → "Add Local Repository"
   - Browse to: `C:\Users\LENOVO\Documents\Cursor apps\Bd tenant`
   - Click "Add Repository"
4. **Publish Repository**:
   - Click "Publish repository"
   - Repository name: `bdtradersv1`
   - Description: "BD Tenant SaaS Platform - Multi-tenant platform for Bangladesh merchants"
   - Make sure "Keep this code private" is unchecked (or checked if you want private)
   - Click "Publish Repository"

---

## Option 3: Using GitHub Web Interface (Manual Upload)

1. **Go to your repository**: https://github.com/NahidDesigner/bdtradersv1
2. **Click "uploading an existing file"** or **"Add file" → "Upload files"**
3. **Drag and drop** all files from your project folder
4. **Commit changes** with message: "Initial commit: BD Tenant SaaS Platform"
5. **Click "Commit changes"**

**Note**: This method is tedious for many files. Use Git or GitHub Desktop instead.

---

## Option 4: Using PowerShell Script (Windows)

I've created a PowerShell script for you. After installing Git:

1. **Open PowerShell** in the project directory
2. **Run the script**:
   ```powershell
   .\push-to-github.ps1
   ```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the script again.

---

## Quick Commands (Copy & Paste)

If Git is installed, copy and paste these commands:

```bash
git init
git add .
git commit -m "Initial commit: BD Tenant SaaS Platform"
git remote add origin https://github.com/NahidDesigner/bdtradersv1.git
git branch -M main
git push -u origin main
```

---

## Troubleshooting

### "git is not recognized"
- Install Git: https://git-scm.com/download/win
- Restart terminal after installation

### "Authentication failed"
- Use Personal Access Token instead of password
- Create token: https://github.com/settings/tokens
- Select `repo` scope

### "Repository not found"
- Check repository URL is correct
- Verify you have write access to the repository
- Make sure repository exists on GitHub

### "Remote origin already exists"
- Remove existing remote: `git remote remove origin`
- Then add again: `git remote add origin https://github.com/NahidDesigner/bdtradersv1.git`

### "Failed to push"
- Make sure repository is empty or you have permission
- Try: `git push -u origin main --force` (⚠️ only if repository is empty)

---

## After Uploading

Once uploaded, you can:

1. **View on GitHub**: https://github.com/NahidDesigner/bdtradersv1
2. **Deploy to Coolify**: Follow `COOLIFY_SETUP.md`
3. **Clone locally**: `git clone https://github.com/NahidDesigner/bdtradersv1.git`

---

## Files Included

The repository includes:
- ✅ Complete backend (FastAPI)
- ✅ Complete frontend (React + Vite)
- ✅ Docker configuration
- ✅ Documentation
- ✅ Coolify setup guides
- ✅ All source code

**Total files**: ~100+ files
**Size**: ~5-10 MB (without node_modules)

---

## Next Steps After Upload

1. ✅ Code is on GitHub
2. 📖 Read `COOLIFY_SETUP.md` for deployment
3. 🚀 Deploy to Coolify
4. 🎉 Your SaaS platform is live!

