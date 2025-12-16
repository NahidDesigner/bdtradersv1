# 🔧 Fix: 503 Service Unavailable Error

## 🔍 The Problem

- ✅ Service is **healthy** in Coolify
- ✅ DNS is configured (Cloudflare)
- ❌ Browser shows **503 Service Unavailable**

This means Coolify's reverse proxy can't reach the frontend container, even though it's healthy.

## ✅ Solution: Expose Ports in Docker Compose

Coolify's reverse proxy needs to know which port to connect to. Let's make it explicit.

### Fix: Add Ports to docker-compose.yaml

The frontend service needs to expose port 80 so Coolify can route to it.

## 🎯 Quick Fix

### Option 1: Add Ports Section (Recommended)

Update `docker-compose.yaml` to explicitly expose ports:

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
    args:
      VITE_API_URL: ${VITE_API_URL}
      VITE_BASE_DOMAIN: ${VITE_BASE_DOMAIN}
  container_name: bd_tenant_frontend
  ports:
    - "80:80"  # Expose port 80
  depends_on:
    - backend
  healthcheck:
    test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1/health"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 40s
  restart: unless-stopped
```

### Option 2: Check Coolify Network Configuration

In Coolify, the reverse proxy should automatically discover services on the same Docker network. But sometimes it needs explicit configuration.

## 🔍 Why 503 Happens

503 Service Unavailable means:
- The reverse proxy (Traefik/Coolify) received the request
- But can't connect to the backend service (frontend container)
- Usually a network/port issue

## ✅ Step-by-Step Fix

### Step 1: Add Ports to docker-compose.yaml

I'll update the docker-compose.yaml to explicitly expose port 80.

### Step 2: Check Coolify Service Configuration

In Coolify → **Configuration**:

1. **Check if frontend service has port configured:**
   - Some Coolify versions need explicit port mapping
   - Look for "Ports" or "Expose" settings

2. **Check network configuration:**
   - Services should be on the same Docker network
   - Coolify should auto-create this

### Step 3: Verify Service is Accessible

In Coolify → **Terminal** → **frontend**:

```bash
# Check if port 80 is listening from outside
netstat -tlnp | grep 80

# Test if service responds
curl http://127.0.0.1/health
```

### Step 4: Check Coolify Proxy Logs

In Coolify → **Logs**:

1. Look for reverse proxy/Traefik logs
2. Check for connection errors
3. Look for "503" or "connection refused" messages

## 🎯 Most Likely Issues

### Issue 1: Port Not Exposed

**Symptom:** Service healthy but 503 error

**Fix:** Add `ports: - "80:80"` to frontend service in docker-compose.yaml

### Issue 2: Network Isolation

**Symptom:** Services can't communicate

**Fix:** Ensure all services are on the same Docker network (Coolify handles this automatically)

### Issue 3: Coolify Proxy Configuration

**Symptom:** Proxy can't find the service

**Fix:** Check if domain is properly assigned to frontend service in Coolify

## 💡 Cloudflare Specific

Since you're using Cloudflare:

1. **Check Cloudflare SSL/TLS mode:**
   - Should be "Full" or "Full (strict)"
   - Not "Flexible" (causes issues)

2. **Check Cloudflare proxy status:**
   - Orange cloud (proxied) - Should work
   - Gray cloud (DNS only) - Should also work

3. **Check for Cloudflare caching:**
   - Try accessing with `?nocache=1`
   - Or purge Cloudflare cache

## 🚀 Immediate Actions

1. **Add ports to docker-compose.yaml** (I'll do this)
2. **Redeploy** in Coolify
3. **Check Cloudflare SSL mode** (should be "Full")
4. **Clear browser cache** or try incognito
5. **Check Coolify logs** for proxy errors

## 🔍 Diagnostic Commands

After adding ports and redeploying:

```bash
# In Coolify Terminal → frontend
netstat -tlnp | grep 80

# Test from inside
curl http://127.0.0.1/health

# Check if accessible from host network
curl -H "Host: bdtraders.vibecodingfield.com" http://localhost/
```

The 503 means the proxy can't reach the container - adding explicit port mapping should fix it!

