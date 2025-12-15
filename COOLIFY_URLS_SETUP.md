# 🌐 URL Configuration for Coolify

## 📋 Quick Answer

Based on your previous setup, here's what to set:

### In Coolify Configuration → Domains:

**Backend Domain:**
```
https://bdtraders.vibecodingfield.com/api
```

**Frontend Domain:**
```
https://bdtraders.vibecodingfield.com/
```

### In Coolify Environment Variables:

**For Frontend Build:**
```
VITE_API_URL = https://bdtraders.vibecodingfield.com/api
VITE_BASE_DOMAIN = bdtraders.vibecodingfield.com
```

## 🎯 Detailed Explanation

### Option 1: Same Domain (Recommended - What You Had)

Both frontend and backend on the same domain:

**Backend:**
- Domain: `https://bdtraders.vibecodingfield.com/api`
- This serves the FastAPI backend at `/api` path

**Frontend:**
- Domain: `https://bdtraders.vibecodingfield.com/`
- This serves the React app at the root

**Environment Variables:**
```
VITE_API_URL = https://bdtraders.vibecodingfield.com/api
VITE_BASE_DOMAIN = bdtraders.vibecodingfield.com
```

**How it works:**
- Frontend loads at: `https://bdtraders.vibecodingfield.com/`
- Frontend calls API at: `https://bdtraders.vibecodingfield.com/api/api/v1/...`
- Backend serves at: `https://bdtraders.vibecodingfield.com/api`

### Option 2: Subdomain (Alternative)

If you prefer separate subdomains:

**Backend:**
- Domain: `https://api.bdtraders.vibecodingfield.com`
- This serves the FastAPI backend

**Frontend:**
- Domain: `https://bdtraders.vibecodingfield.com`
- This serves the React app

**Environment Variables:**
```
VITE_API_URL = https://api.bdtraders.vibecodingfield.com
VITE_BASE_DOMAIN = bdtraders.vibecodingfield.com
```

## 📝 Step-by-Step in Coolify

1. **Go to Configuration → General**

2. **Set Backend Domain:**
   - Find "Domains for backend"
   - Enter: `https://bdtraders.vibecodingfield.com/api`
   - Or click "Generate Domain" if Coolify suggests one

3. **Set Frontend Domain:**
   - Find "Domains for frontend"
   - Enter: `https://bdtraders.vibecodingfield.com/`
   - Or click "Generate Domain" if Coolify suggests one

4. **Go to Environment Variables**

5. **Set VITE_API_URL:**
   - Variable: `VITE_API_URL`
   - Value: `https://bdtraders.vibecodingfield.com/api`
   - **Important:** Check "Available at Buildtime" ✅
   - This is needed because Vite bakes this into the build

6. **Set VITE_BASE_DOMAIN (Optional):**
   - Variable: `VITE_BASE_DOMAIN`
   - Value: `bdtraders.vibecodingfield.com`
   - **Important:** Check "Available at Buildtime" ✅

7. **Save and Deploy**

## ⚠️ Important Notes

1. **VITE_API_URL must be set at build time**
   - Check "Available at Buildtime" in Coolify
   - This is baked into the frontend build
   - If you change it later, you need to rebuild

2. **No trailing slash for VITE_API_URL**
   - ✅ Correct: `https://bdtraders.vibecodingfield.com/api`
   - ❌ Wrong: `https://bdtraders.vibecodingfield.com/api/`

3. **Backend path structure:**
   - Backend serves at: `/api/v1/...`
   - So if backend domain is `/api`, full path is `/api/api/v1/...`
   - Frontend code adds `/api/v1` automatically

4. **CORS Configuration:**
   - Make sure `CORS_ORIGINS` includes your frontend domain
   - Or set it to `*` for development (default)

## 🔍 How to Verify

After deployment:

1. **Check Frontend:**
   - Visit: `https://bdtraders.vibecodingfield.com/`
   - Should see the login page

2. **Check Backend:**
   - Visit: `https://bdtraders.vibecodingfield.com/api/health`
   - Should see: `{"status":"healthy","service":"bd-tenant-backend"}`

3. **Check API Connection:**
   - Open browser console on frontend
   - Try to login
   - Check Network tab - API calls should go to `/api/api/v1/...`

## 🎯 Recommended Setup (What You Had)

```
Backend Domain:  https://bdtraders.vibecodingfield.com/api
Frontend Domain: https://bdtraders.vibecodingfield.com/
VITE_API_URL:    https://bdtraders.vibecodingfield.com/api
```

This is the simplest and works great!

