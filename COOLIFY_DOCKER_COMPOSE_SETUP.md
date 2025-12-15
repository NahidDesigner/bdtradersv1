# Coolify Docker Compose Configuration

## ⚠️ Important: Use Docker Compose Mode

This project uses **Docker Compose** with multiple services (backend, frontend, postgres). 

Coolify needs to be configured to use **Docker Compose mode**, not a single Dockerfile.

## ✅ Correct Setup in Coolify

### Step 1: Create Resource Type

1. In Coolify, when creating a new resource:
2. **Select**: "Docker Compose" (NOT "Dockerfile")
3. Connect your GitHub repository: `NahidDesigner/bdtradersv1`
4. Select branch: `main`

### Step 2: Coolify Will Auto-Detect

Coolify should automatically detect `docker-compose.yml` in the root directory.

### Step 3: Configure Services

Coolify will show you all services from docker-compose.yml:
- `postgres` - Database
- `backend` - FastAPI backend
- `frontend` - React frontend

### Step 4: Set Environment Variables

For each service, set the required environment variables (see `COOLIFY_SETUP.md`).

### Step 5: Configure Domains

- **Frontend service**: Set domain (e.g., `app.yourdomain.com`)
- **Backend service**: Set domain (e.g., `api.yourdomain.com`)

## 🔧 If Coolify Shows "Dockerfile" Error

If you see the error:
```
ERROR: failed to build: failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory
```

**Solution:**
1. Go to your resource settings in Coolify
2. Check the **Build Pack** or **Deployment Type**
3. Make sure it's set to **"Docker Compose"** not **"Dockerfile"**
4. If there's no Docker Compose option, you may need to:
   - Delete the resource
   - Create a new one
   - Select "Docker Compose" from the start

## 📋 Alternative: Single Service Deployment

If Coolify doesn't support Docker Compose well, you can deploy services separately:

### Option 1: Deploy Backend Only First

1. Create a resource pointing to `backend/Dockerfile`
2. Set working directory to `backend/`
3. Configure environment variables
4. Deploy

### Option 2: Use Production Compose File

We have `docker-compose.prod.yml` which is optimized for production. You can:
1. Rename it to `docker-compose.yml`
2. Or configure Coolify to use it specifically

## 🚀 Quick Fix

If you're seeing the Dockerfile error right now:

1. **In Coolify Dashboard:**
   - Go to your resource settings
   - Look for "Build Pack" or "Build Configuration"
   - Change from "Dockerfile" to "Docker Compose"
   - Save and redeploy

2. **Or create a new resource:**
   - Delete the current one
   - Create new → Select "Docker Compose"
   - Connect same repository
   - Configure services

## ✅ Verification

After configuring Docker Compose mode, you should see:
- Multiple services listed (postgres, backend, frontend)
- Ability to set environment variables per service
- Ability to configure domains per service
- Build should succeed

## 📚 Reference

- Main setup guide: `COOLIFY_SETUP.md`
- Quick start: `QUICK_START_COOLIFY.md`
- Architecture: `ARCHITECTURE.md`

