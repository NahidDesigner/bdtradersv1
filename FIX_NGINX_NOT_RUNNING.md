# 🔧 Fix: Nginx Not Running - Connection Refused

## 🔍 The Problem

Terminal shows:
```
wget: can't connect to remote host: Connection refused
```

This means **nginx is not running** or **not listening on port 80** inside the frontend container.

## ✅ Diagnostic Steps

### Step 1: Check if Nginx is Running

In Coolify → **Terminal** → **frontend** service:

```bash
ps aux | grep nginx
```

**Expected:** Should show nginx processes
**If empty:** Nginx is not running

### Step 2: Check if Port 80 is Listening

```bash
netstat -tlnp | grep 80
# OR
ss -tlnp | grep 80
```

**Expected:** Should show port 80 is listening
**If empty:** Nothing is listening on port 80

### Step 3: Check Nginx Process

```bash
# Check if nginx master process exists
pgrep nginx

# Check nginx status
nginx -t
```

### Step 4: Check if Files Exist

```bash
ls -la /usr/share/nginx/html/
```

**Expected:** Should show `index.html` and other files
**If empty:** Build failed - no files to serve

### Step 5: Try Starting Nginx Manually

```bash
# Start nginx
nginx

# Check if it starts
ps aux | grep nginx
```

## 🎯 Most Likely Issues

### Issue 1: Nginx Not Starting

**Symptom:** `ps aux | grep nginx` returns nothing

**Possible causes:**
- Nginx configuration error
- Port 80 already in use
- Missing files

**Fix:**
```bash
# Check nginx config
nginx -t

# If error, check config file
cat /etc/nginx/conf.d/default.conf

# Try starting nginx manually
nginx -g "daemon off;"
```

### Issue 2: Build Failed - No Files

**Symptom:** `/usr/share/nginx/html/` is empty

**Fix:** Check build logs in Coolify → Deployments

### Issue 3: Port Conflict

**Symptom:** Port 80 already in use

**Fix:** Check what's using port 80:
```bash
lsof -i :80
# OR
netstat -tlnp | grep 80
```

## ✅ Quick Fixes

### Fix 1: Check Nginx Logs

```bash
# Check nginx error log
cat /var/log/nginx/error.log

# Check if log exists
ls -la /var/log/nginx/
```

### Fix 2: Verify Nginx Config

```bash
# Test nginx configuration
nginx -t

# View nginx config
cat /etc/nginx/conf.d/default.conf
```

### Fix 3: Check Container Entrypoint

The Dockerfile should start nginx with:
```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

Verify this is correct.

### Fix 4: Check if Build Succeeded

```bash
# Check if dist folder has files
ls -la /usr/share/nginx/html/

# Check index.html
head -20 /usr/share/nginx/html/index.html
```

## 🚀 Step-by-Step Fix

### Step 1: Check What's Wrong

Run these commands in Terminal → frontend:

```bash
# 1. Check if nginx is running
ps aux | grep nginx

# 2. Check if files exist
ls -la /usr/share/nginx/html/

# 3. Check nginx config
nginx -t

# 4. Check error logs
cat /var/log/nginx/error.log 2>/dev/null || echo "No error log"
```

### Step 2: Try to Start Nginx

```bash
# Start nginx in foreground to see errors
nginx -g "daemon off;" &
```

### Step 3: Check Build

If files don't exist, the build failed. Check:
- Coolify → Deployments → Latest deployment
- Look for frontend build errors
- Check if `npm run build` succeeded

## 💡 Alternative: Health Check Issue

If nginx IS running but health check fails, the issue might be:

1. **Health check runs too early** - nginx needs time to start
2. **Health check command wrong** - `wget` might not work
3. **Health endpoint not configured** - `/health` might not exist

**Fix health check:**
- Current: `wget --quiet --tries=1 --spider http://localhost/`
- Try: `curl -f http://localhost/health || exit 1`

## 🔍 What to Check

Run these in Terminal → frontend and share results:

1. `ps aux | grep nginx` - Is nginx running?
2. `ls -la /usr/share/nginx/html/` - Do files exist?
3. `nginx -t` - Is config valid?
4. `cat /var/log/nginx/error.log` - Any errors?

This will tell us exactly what's wrong!

