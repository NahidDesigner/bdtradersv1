# 🔧 Fix: Coolify Routing - Frontend Not Serving

## 🔍 The Problem

Coolify is routing ALL requests (including `/`) to the backend instead of routing:
- `/api/*` → Backend
- `/*` → Frontend

## ✅ Solution: Use Separate Subdomains (Easiest)

### Option 1: Separate Subdomains (Recommended)

**In Coolify → Configuration → General → Domains:**

1. **Backend Domain:**
   ```
   https://api.bdtraders.vibecodingfield.com
   ```
   (No `/api` path - just the subdomain)

2. **Frontend Domain:**
   ```
   https://bdtraders.vibecodingfield.com
   ```
   (Root domain)

3. **Update Environment Variables:**
   ```
   VITE_API_URL = https://api.bdtraders.vibecodingfield.com
   VITE_BASE_DOMAIN = bdtraders.vibecodingfield.com
   ```
   (Check "Available at Buildtime" ✅)

4. **Redeploy** to rebuild frontend with new API URL

### Option 2: Keep Same Domain (Requires Coolify Configuration)

If you want to keep `/api` for backend:

1. **Backend Domain:**
   ```
   https://bdtraders.vibecodingfield.com/api
   ```

2. **Frontend Domain:**
   ```
   https://bdtraders.vibecodingfield.com
   ```
   (Just the domain, NO path)

3. **In Coolify, you may need to:**
   - Check "Advanced" settings
   - Ensure routing priority: Frontend first, then Backend
   - Or use a custom nginx configuration

## 🎯 Why This Happens

Coolify's reverse proxy routes based on domain configuration. When both services are on the same domain:
- If frontend domain is set incorrectly, Coolify routes everything to backend
- If routing priority is wrong, backend catches all requests

## ✅ Quick Fix Steps

### Step 1: Change to Separate Subdomains

1. **In Coolify → Configuration → General:**
   - Backend Domain: `https://api.bdtraders.vibecodingfield.com`
   - Frontend Domain: `https://bdtraders.vibecodingfield.com`

2. **In Coolify → Environment Variables:**
   - `VITE_API_URL` = `https://api.bdtraders.vibecodingfield.com`
   - `VITE_BASE_DOMAIN` = `bdtraders.vibecodingfield.com`
   - Check "Available at Buildtime" ✅

3. **Redeploy** (this rebuilds frontend with new API URL)

### Step 2: Verify DNS

Make sure both subdomains point to your server:
- `api.bdtraders.vibecodingfield.com` → Your server IP
- `bdtraders.vibecodingfield.com` → Your server IP

### Step 3: Test

After redeploy:
- `https://bdtraders.vibecodingfield.com/` → Should show login page
- `https://api.bdtraders.vibecodingfield.com/health` → Should return JSON

## 🔍 Alternative: Check Coolify Advanced Settings

If you want to keep same domain:

1. Go to **Configuration → Advanced**
2. Look for routing/priority settings
3. Set frontend to handle `/` first
4. Set backend to handle `/api/*` only

But **separate subdomains is much easier and more reliable!**

## 📋 Checklist

- [ ] Backend domain: `https://api.bdtraders.vibecodingfield.com`
- [ ] Frontend domain: `https://bdtraders.vibecodingfield.com`
- [ ] `VITE_API_URL` = `https://api.bdtraders.vibecodingfield.com`
- [ ] `VITE_BASE_DOMAIN` = `bdtraders.vibecodingfield.com`
- [ ] Both variables have "Available at Buildtime" checked
- [ ] DNS records set for both subdomains
- [ ] Redeployed after changes

## 🚀 After Fixing

1. Frontend will be at: `https://bdtraders.vibecodingfield.com/`
2. Backend will be at: `https://api.bdtraders.vibecodingfield.com/`
3. Frontend will call backend at: `https://api.bdtraders.vibecodingfield.com/api/v1/...`

This is the cleanest solution and avoids routing conflicts!

