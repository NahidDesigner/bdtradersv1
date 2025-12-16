# 🔧 Fix: Nginx Running But Port 80 Not Listening

## 🔍 The Problem

Diagnostic shows:
- ✅ Nginx IS running (master + 2 workers)
- ✅ Files exist (index.html, assets, etc.)
- ✅ Nginx config is valid
- ❌ Port 80 is NOT listening!

This is why health check fails - nginx is running but not bound to port 80.

## ✅ Diagnostic Commands

Run these in Terminal → frontend:

### Check What Nginx is Listening On

```bash
# Check all listening ports
netstat -tlnp

# OR use ss (more modern)
ss -tlnp

# Check specifically for nginx
ss -tlnp | grep nginx

# Check IPv6
ss -tlnp | grep :80
```

### Check Nginx Listen Configuration

```bash
# Check what nginx config says
grep -i listen /etc/nginx/conf.d/default.conf

# Check main nginx config
cat /etc/nginx/nginx.conf | grep -A 5 -B 5 listen
```

### Test Connection Directly

```bash
# Try connecting to localhost:80
curl -v http://localhost/

# Try IPv4 specifically
curl -v http://127.0.0.1/

# Try IPv6
curl -v http://[::1]/
```

## 🎯 Most Likely Issue

Nginx might be:
1. **Listening on IPv6 only** (::80) not IPv4 (0.0.0.0:80)
2. **Not binding to 0.0.0.0** - only binding to specific interface
3. **Port conflict** - something else using port 80

## ✅ Quick Fix: Update Nginx Config

The nginx.conf has `listen 80;` which should work, but let's make it explicit:

### Fix 1: Explicitly Bind to All Interfaces

Update `frontend/nginx.conf`:

```nginx
server {
    listen 0.0.0.0:80;  # Explicitly bind to all IPv4 interfaces
    listen [::]:80;      # Also bind to IPv6
    server_name _;
    # ... rest of config
}
```

### Fix 2: Check if Port is Already in Use

```bash
# Check what's using port 80
lsof -i :80

# OR
fuser 80/tcp
```

## 🚀 Step-by-Step Fix

### Step 1: Check Current Listen Status

```bash
# See what nginx is actually listening on
ss -tlnp | grep nginx
```

### Step 2: Check Nginx Config

```bash
# See what the config says
grep listen /etc/nginx/conf.d/default.conf
```

### Step 3: Test Connection

```bash
# Try different connection methods
curl http://127.0.0.1/
curl http://localhost/
curl http://0.0.0.0/
```

### Step 4: Fix Config if Needed

If nginx is only listening on IPv6 or specific interface, we need to update the config to explicitly listen on 0.0.0.0:80.

## 💡 Alternative: Health Check Issue

If nginx IS listening but health check still fails, the issue might be:

1. **Health check uses wrong address** - `localhost` might resolve to IPv6
2. **Health check timing** - runs before nginx fully starts
3. **Health check command** - `wget` might have issues

**Try different health check:**
```bash
# Test health endpoint
curl -f http://127.0.0.1/health

# Test root
curl -f http://127.0.0.1/
```

## 🔍 What to Check Now

Run these commands and share results:

1. `ss -tlnp | grep nginx` - What is nginx listening on?
2. `curl -v http://127.0.0.1/` - Does curl work?
3. `grep listen /etc/nginx/conf.d/default.conf` - What does config say?

This will tell us exactly why port 80 isn't showing up in netstat!

