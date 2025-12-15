# 🚨 URGENT: Frontend "no available server" - Coolify Configuration Fix

## 🔍 The Problem

All containers are running (logs show nginx, postgres, backend all healthy), but the frontend shows "no available server". This means **Coolify isn't routing requests to the frontend container**.

## ✅ Solution: Fix Coolify Service Configuration

### Step 1: Check Service Ports in Coolify

In Coolify, each service needs to expose its port:

1. **Go to your project** → **Configuration**
2. **Check if services are properly configured:**
   - **Frontend service** should expose port **80**
   - **Backend service** should expose port **8000**

### Step 2: Verify Frontend Service is Exposed

In Coolify → **Configuration → General**:

1. **Check "Ports" or "Expose" settings:**
   - Frontend should expose: `80:80` or just `80`
   - Backend should expose: `8000:8000` or just `8000`

2. **If ports aren't exposed:**
   - Go to **Advanced** settings
   - Add port mapping for frontend: `80`
   - Add port mapping for backend: `8000`

### Step 3: Check Domain Configuration (Critical!)

In Coolify → **Configuration → General → Domains**:

**Option A: If using same domain (current setup):**

1. **Backend Domain:**
   ```
   https://bdtraders.vibecodingfield.com/api
   ```
   - Make sure it's set to `/api` path

2. **Frontend Domain:**
   ```
   https://bdtraders.vibecodingfield.com
   ```
   - **IMPORTANT:** Just the domain, NO trailing slash, NO path
   - Should be exactly: `bdtraders.vibecodingfield.com` (Coolify adds https://)

**Option B: If using subdomains (recommended):**

1. **Backend Domain:**
   ```
   api.bdtraders.vibecodingfield.com
   ```

2. **Frontend Domain:**
   ```
   bdtraders.vibecodingfield.com
   ```

### Step 4: Verify Service is Selected for Domain

In Coolify, when you set a domain, you need to **select which service** it routes to:

1. **For Frontend Domain:**
   - Make sure it's routing to the **frontend** service
   - NOT the backend service

2. **For Backend Domain:**
   - Make sure it's routing to the **backend** service

### Step 5: Check if Frontend Service is Enabled

1. In Coolify → **Configuration**
2. Make sure **frontend** service is:
   - ✅ Enabled
   - ✅ Running
   - ✅ Has a domain assigned

### Step 6: Restart/Redeploy

After making changes:

1. **Save** all configuration
2. **Redeploy** the application
3. Wait for all services to start

## 🔍 Debugging Steps

### Test 1: Check if Frontend Container is Accessible Internally

In Coolify → **Terminal** tab:

1. Select **frontend** service
2. Run: `wget -O- http://localhost/health`
   - Should return: `healthy`
   - If this works, container is fine, issue is routing

### Test 2: Check Backend is Accessible

Visit: `https://bdtraders.vibecodingfield.com/api/health`
- ✅ Should return JSON (this is working based on your logs)

### Test 3: Check Frontend Health Endpoint

Visit: `https://bdtraders.vibecodingfield.com/health`
- ✅ Should return: `healthy`
- ❌ If "no available server" → Routing issue

## 🎯 Most Common Issues

### Issue 1: Frontend Domain Not Assigned to Frontend Service

**Fix:** In Coolify, make sure the frontend domain is assigned to the **frontend** service, not backend.

### Issue 2: Port Not Exposed

**Fix:** Make sure frontend service exposes port 80 in Coolify configuration.

### Issue 3: Domain Configuration Wrong

**Fix:** Frontend domain should be just the domain name (no path, no trailing slash).

### Issue 4: Service Not Running

**Fix:** Check logs - if frontend container isn't running, restart it.

## ✅ Quick Checklist

- [ ] Frontend service is enabled in Coolify
- [ ] Frontend service exposes port 80
- [ ] Frontend domain is set to: `bdtraders.vibecodingfield.com` (no path)
- [ ] Frontend domain is assigned to **frontend** service (not backend)
- [ ] Backend domain is set to: `bdtraders.vibecodingfield.com/api` or `api.bdtraders.vibecodingfield.com`
- [ ] All services are running (check logs)
- [ ] Redeployed after configuration changes

## 🚀 Alternative: Check Coolify Service List

In Coolify, you should see **3 services**:
1. **postgres** - Database
2. **backend** - API server
3. **frontend** - Web app

Make sure all 3 are:
- ✅ Running
- ✅ Have proper domains assigned
- ✅ Have ports exposed

## 💡 If Still Not Working

Try accessing the frontend directly by IP (if you know it):
- `http://YOUR_SERVER_IP:PORT` (if port is exposed)

Or check Coolify's **Links** tab to see what URLs are actually configured.

The containers are running fine - this is purely a Coolify routing/domain configuration issue!

