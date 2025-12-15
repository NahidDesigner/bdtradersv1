# 🔧 Fix: "Running (unhealthy)" Status in Coolify

## 🔍 The Problem

Your domains are correctly configured:
- ✅ Backend: `api.bdtraders.vibecodingfield.com`
- ✅ Frontend: `bdtraders.vibecodingfield.com`
- ✅ All 3 services are detected

But the status shows **"Running (unhealthy)"** - this is why the frontend isn't accessible!

## ✅ Solution: Fix Health Checks

The health check is failing. Let's check and fix it.

### Step 1: Check Which Service is Unhealthy

In Coolify → **Logs** tab:

1. **Click on each service** to expand logs:
   - `frontend-...`
   - `backend-...`
   - `postgres-...`

2. **Look for health check errors:**
   - Should see health check attempts
   - Look for failures or timeouts

### Step 2: Test Frontend Health Check Manually

In Coolify → **Terminal** tab:

1. **Select `frontend` service** from dropdown
2. **Run:** `wget -O- http://localhost/health`
   - ✅ Should return: `healthy`
   - ❌ If it fails → Health check endpoint issue

### Step 3: Check Health Check Configuration

The frontend health check in `docker-compose.yaml` uses:
```yaml
test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
```

This checks if nginx is serving the root path. If this fails, the service is marked unhealthy.

### Step 4: Verify Frontend is Actually Serving

In Coolify → **Terminal** tab → **frontend** service:

1. **Run:** `ls -la /usr/share/nginx/html/`
   - Should show `index.html` and other files
   - If empty → Build failed

2. **Run:** `cat /usr/share/nginx/html/index.html`
   - Should show HTML content
   - If empty → Build issue

### Step 5: Check Nginx Configuration

In Coolify → **Terminal** tab → **frontend** service:

1. **Run:** `cat /etc/nginx/conf.d/default.conf`
   - Should show nginx configuration
   - Check if it's correct

2. **Run:** `nginx -t`
   - Should say "syntax is ok"
   - If error → Nginx config issue

## 🎯 Most Likely Issues

### Issue 1: Health Check Too Strict

The health check might be failing because:
- Nginx takes time to start
- Health check runs before nginx is ready
- `wget` might not be installed

**Fix:** The health check has `start_period: 40s` which should help, but might need more time.

### Issue 2: Frontend Build Failed

If the frontend build failed:
- `dist/` folder might be empty
- No `index.html` to serve
- Health check fails because there's nothing to serve

**Fix:** Check build logs in Coolify deployment logs.

### Issue 3: Health Check Command Failing

The `wget` command might not work:
- `wget` might not be in the nginx:alpine image
- Command syntax might be wrong

**Fix:** We might need to change the health check command.

## ✅ Quick Fixes

### Fix 1: Check Frontend Build

In Coolify → **Deployments** tab:
1. Look at the latest deployment
2. Check frontend build logs
3. Look for errors during `npm run build`

### Fix 2: Test Health Endpoint

In Coolify → **Terminal** → **frontend** service:

```bash
# Test if nginx is running
ps aux | grep nginx

# Test if port 80 is listening
netstat -tlnp | grep 80

# Test health endpoint
curl http://localhost/health
```

### Fix 3: Check if Files Exist

```bash
# Check if build output exists
ls -la /usr/share/nginx/html/

# Check index.html
cat /usr/share/nginx/html/index.html | head -20
```

## 🔍 Diagnostic Steps

1. **Check which service is unhealthy:**
   - Expand each service in Logs
   - Look for health check failures

2. **Check frontend build:**
   - Look at deployment logs
   - Check if `npm run build` succeeded

3. **Test frontend manually:**
   - Use Terminal to test health endpoint
   - Check if nginx is serving files

## 🚀 After Fixing

Once health checks pass:
- Status should change to "Running (healthy)"
- Frontend should be accessible at `https://bdtraders.vibecodingfield.com/`
- Backend should be accessible at `https://api.bdtraders.vibecodingfield.com/`

The domains are correct - we just need to fix the health check issue!

