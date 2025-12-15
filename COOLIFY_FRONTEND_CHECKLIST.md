# ✅ Coolify Frontend Configuration - Step-by-Step Checklist

## 🔍 Current Status

✅ All containers are running:
- Frontend (nginx) - Running
- Backend (FastAPI) - Running and healthy
- Postgres - Running

❌ Frontend shows "no available server" - This is a **Coolify routing issue**

## 📋 Step-by-Step Fix in Coolify

### Step 1: Verify Services Exist

In Coolify → Your Project:

1. You should see **3 services** listed:
   - `postgres` (or `bd_tenant_db`)
   - `backend` (or `bd_tenant_backend`)
   - `frontend` (or `bd_tenant_frontend`)

2. **If frontend service is missing:**
   - Coolify might not have detected it from docker-compose
   - Check if docker-compose.yaml is being read correctly
   - Try redeploying

### Step 2: Check Domain Configuration

In Coolify → **Configuration → General → Domains**:

**For Frontend:**
1. Find "Domains for frontend" or "Frontend Domain"
2. Should be set to: `bdtraders.vibecodingfield.com`
   - ✅ Correct: `bdtraders.vibecodingfield.com`
   - ❌ Wrong: `https://bdtraders.vibecodingfield.com/` (no https://, no trailing slash)
   - ❌ Wrong: `bdtraders.vibecodingfield.com/` (no trailing slash)

**For Backend:**
1. Find "Domains for backend" or "Backend Domain"
2. Should be set to: `bdtraders.vibecodingfield.com/api` OR `api.bdtraders.vibecodingfield.com`

### Step 3: Verify Service Assignment

**Critical:** Make sure domains are assigned to the correct services:

1. **Frontend Domain** → Should route to **frontend** service
2. **Backend Domain** → Should route to **backend** service

**How to check:**
- In Coolify, when you click on a domain, it should show which service it's assigned to
- Or look for a dropdown/selector next to each domain

### Step 4: Check Port Configuration

In Coolify → **Configuration → Advanced** (or Ports section):

1. **Frontend service:**
   - Should expose port: `80`
   - Format: `80:80` or just `80`

2. **Backend service:**
   - Should expose port: `8000`
   - Format: `8000:8000` or just `8000`

### Step 5: Check Service Status

In Coolify → **Logs** or **Services**:

1. **Frontend service:**
   - Status: Should be "Running" or "Healthy"
   - If "Stopped" or "Unhealthy" → Restart it

2. **Backend service:**
   - Status: Should be "Running" or "Healthy"
   - ✅ This is working (based on your logs)

### Step 6: Test Internal Connectivity

In Coolify → **Terminal** tab:

1. Select **frontend** service from dropdown
2. Run: `wget -O- http://localhost/health`
   - ✅ Should return: `healthy`
   - ✅ If this works → Container is fine, issue is routing
   - ❌ If this fails → Container issue

### Step 7: Check Links/URLs

In Coolify → **Links** tab (or similar):

1. Should show:
   - Frontend URL: `https://bdtraders.vibecodingfield.com`
   - Backend URL: `https://bdtraders.vibecodingfield.com/api` or `https://api.bdtraders.vibecodingfield.com`

2. **Click the frontend link** - Does it work?

### Step 8: Redeploy After Changes

After making any configuration changes:

1. **Save** all settings
2. Click **"Redeploy"** or **"Deploy"**
3. Wait for all services to start
4. Check logs to confirm all services are running

## 🎯 Most Common Issues

### Issue 1: Frontend Domain Not Set
**Symptom:** No domain assigned to frontend service
**Fix:** Set frontend domain in Coolify configuration

### Issue 2: Domain Assigned to Wrong Service
**Symptom:** Frontend domain routes to backend
**Fix:** Reassign domain to frontend service

### Issue 3: Port Not Exposed
**Symptom:** Frontend container running but not accessible
**Fix:** Expose port 80 for frontend service

### Issue 4: DNS Not Configured
**Symptom:** Domain doesn't resolve
**Fix:** Check DNS settings for `bdtraders.vibecodingfield.com`

## 🔍 Quick Diagnostic

Run these tests:

1. **Backend health (should work):**
   ```
   https://bdtraders.vibecodingfield.com/api/health
   ```
   ✅ Should return JSON

2. **Frontend health (might not work):**
   ```
   https://bdtraders.vibecodingfield.com/health
   ```
   ✅ Should return: `healthy`
   ❌ If "no available server" → Routing issue

3. **Frontend root (should work after fix):**
   ```
   https://bdtraders.vibecodingfield.com/
   ```
   ✅ Should show login page
   ❌ If "no available server" → Routing issue

## 💡 Alternative: Check Coolify Version

Some Coolify versions handle Docker Compose routing differently:

1. Check your Coolify version
2. If using an older version, try updating
3. Or check Coolify documentation for Docker Compose routing

## 🚀 If Nothing Works

As a last resort:

1. **Delete the project** in Coolify
2. **Create a new project**
3. **Connect to the same GitHub repo**
4. **Set domains correctly from the start:**
   - Frontend: `bdtraders.vibecodingfield.com`
   - Backend: `api.bdtraders.vibecodingfield.com` (use subdomain)
5. **Deploy**

This ensures a clean configuration.

## ✅ Success Criteria

After fixing, you should be able to:

1. ✅ Visit `https://bdtraders.vibecodingfield.com/` → See login page
2. ✅ Visit `https://bdtraders.vibecodingfield.com/health` → See "healthy"
3. ✅ Visit `https://bdtraders.vibecodingfield.com/api/health` → See JSON
4. ✅ All services show "Running" in Coolify

The containers are working perfectly - this is purely a Coolify configuration issue!

